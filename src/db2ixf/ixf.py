# coding=utf-8
"""Creates an PC/IXF parser"""
from __future__ import annotations

import csv
import deltalake
import json
import pyarrow as pa
from db2ixf.collectors import (
    collect_bigint, collect_binary, collect_blob, collect_char, collect_clob,
    collect_date, collect_decimal, collect_floating_point, collect_integer,
    collect_longvarchar, collect_smallint, collect_time, collect_timestamp,
    collect_varchar, collect_vargraphic,
)
from db2ixf.constants import (
    COL_DESCRIPTOR_RECORD_TYPE, DATA_RECORD_TYPE, DB2IXF_ACCEPTED_CORRUPTION_RATE, HEADER_RECORD_TYPE,
    TABLE_RECORD_TYPE,
)
from db2ixf.encoders import CustomJSONEncoder
from db2ixf.exceptions import (
    DataCollectorError, IXFParsingError, NotValidColumnDescriptorException, UnknownDataTypeException,
)
from db2ixf.helpers import (
    apply_schema_fixes, get_pyarrow_schema, pyarrow_record_batches,
)
from db2ixf.logger import logger
from deltalake import DeltaTable
from os import PathLike
from pathlib import Path
from pyarrow.parquet import ParquetWriter
from typing import (
    Any, BinaryIO, Dict, Iterable, List, Literal, Optional, TextIO, Tuple, Union,
)


class IXFParser:
    """
    PC/IXF Parser.

    Attributes
    ----------
    file : str, Path, PathLike or File-Like Object
        Input file and it is better to use file-like object.
    """
    header_info: dict
    """Contains header informations from input ixf file."""
    table_info: dict
    """Contains table informations from input ixf file."""
    columns_info: List[dict]
    """Contains columns description from input ixf file."""
    pyarrow_schema: pa.Schema
    """Schema extracted from metadata in the input ixf file and converted to parquet one."""
    current_data_record: dict
    """Contains current data record from input ixf file."""
    end_data_records: bool
    """Flag the end of data records in the input ixf file."""
    current_row: dict
    """Contains parsed data extracted from a data record of the input ixf file."""
    number_rows: int
    """Number of rows extracted from the input ixf file."""
    number_corrupted_rows: int
    """Number of corrupted rows that contain data we can not parse or handle."""

    def __init__(self, file: Union[str, Path, PathLike, BinaryIO]):
        """Init the instance."""
        if isinstance(file, (str, Path, PathLike)):
            file = open(file, mode="rb")
            logger.debug("File opened in read & binary mode")

        if file.mode != "rb":
            msg = "file-like object should be opened in read-binary mode"
            raise ValueError(msg)

        # Init instance attributes
        self.file = file

        # State
        self.header_info = {}
        self.table_info = {}
        self.columns_info = []
        self.pyarrow_schema = pa.schema([])
        self.current_data_record = {}
        self.end_data_records = False
        self.current_row = {}
        self.number_rows = 0
        self.number_corrupted_rows = -1  # Avoids counting the last line (EOF)

    def parse_header(self, record_type: dict = None) -> dict:
        """Parse the header record.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Returns
        -------
        dict
            Header record of the input file.
        """
        if record_type is None:
            record_type = HEADER_RECORD_TYPE

        for u, w in record_type.items():
            self.header_info[u] = self.file.read(w)

        return self.header_info

    def parse_table(self, record_type: dict = None) -> dict:
        """Parse the table record.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Returns
        -------
        dict
            Table record of the input file.
        """
        if record_type is None:
            record_type = TABLE_RECORD_TYPE

        for m, n in record_type.items():
            self.table_info[m] = self.file.read(n)

        return self.table_info

    def parse_columns(self, record_type: dict = None) -> List[dict]:
        """Parse the column records.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Returns
        -------
        list
            Column descriptors records of the input file.

        Raises
        ------
        NotValidColumnDescriptorException
            If the IXF contains a non valid column descriptor.
        """
        if record_type is None:
            record_type = COL_DESCRIPTOR_RECORD_TYPE

        # "IXFTCCNT" contains number of columns in the table
        for _ in range(0, int(self.table_info["IXFTCCNT"])):

            column = {}
            for i, j in record_type.items():
                column[i] = self.file.read(j)

            if column["IXFCRECT"] != b"C":
                msg1 = f"Non valid IXF file: It either contains non " \
                       f"supported record type/subtype like application " \
                       f"one or it contains a non valid column descriptor " \
                       f"(see the column {column['IXFCNAME']})."
                logger.error(msg1)
                msg2 = "Hint: try to recreate IXF file without any " \
                       "application record or any SQL error."
                logger.info(msg2)
                raise NotValidColumnDescriptorException(msg1)

            column["IXFCDSIZ"] = self.file.read(int(column["IXFCRECL"]) - 862)

            self.columns_info.append(column)

        return self.columns_info

    def get_data_record(self, record_type: dict = None):
        """get one data record.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Returns
        ------
        dict
            Dictionary containing current data record from IXF file.
        """
        if record_type is None:
            record_type = DATA_RECORD_TYPE

        self.current_data_record = {}
        for key, val in record_type.items():
            self.current_data_record[key] = self.file.read(val)

        self.current_data_record["IXFDCOLS"] = self.file.read(
            int(self.current_data_record["IXFDRECL"]) - 8
        )
        return self.current_data_record

    def collect_data(self) -> dict:
        """collect data from fields of the current data record.

        Returns
        -------
        dict:
            Dictionary containing all extracted data from fields of
            the data record.
        """
        # Start Extraction
        try:
            r = {}
            for c in self.columns_info:
                col_name = str(c["IXFCNAME"], encoding="utf-8").strip()
                col_type = int(c["IXFCTYPE"])
                col_is_nullable = c["IXFCNULL"] == b"Y"
                col_position = int(c["IXFCPOSN"])

                # Parse next data record in case a column is in position 1
                if col_position == 1:
                    self.get_data_record()

                # Mark the end of data records: helps exit the while loop
                if self.current_data_record["IXFDRECT"] != b"D":
                    self.end_data_records = True
                    logger.debug("End of data records")
                    break

                # Position index is then equals to position - 1
                pos = col_position - 1

                # Handle nullable
                if col_is_nullable:
                    # Column is null
                    if self.current_data_record["IXFDCOLS"][pos:pos + 2] == b"\xff\xff":
                        r[col_name] = None
                        continue
                    # Column is not null
                    elif self.current_data_record["IXFDCOLS"][pos:pos + 2] == b"\x00\x00":
                        pos += 2

                # Collect data
                switcher = {
                    384: collect_date,
                    388: collect_time,
                    392: collect_timestamp,
                    404: collect_blob,
                    408: collect_clob,
                    448: collect_varchar,
                    452: collect_char,
                    456: collect_longvarchar,
                    464: collect_vargraphic,
                    480: collect_floating_point,
                    484: collect_decimal,
                    492: collect_bigint,
                    496: collect_integer,
                    500: collect_smallint,
                    912: collect_binary,
                }

                _func = switcher.get(col_type, None)
                if _func is None:
                    msg = f"The column {col_name} has unknown data type {col_type}"
                    raise UnknownDataTypeException(msg)

                r[col_name] = _func(c, self.current_data_record["IXFDCOLS"], pos)
            return r
        except UnknownDataTypeException as er1:
            logger.error(er1)
            raise IXFParsingError(er1)
        except DataCollectorError as er2:
            logger.error(er2)
            return {}
        except Exception as er3:
            logger.error(er3)
            raise IXFParsingError(er3)

    def parse_data(self) -> Iterable[Dict]:
        """Parse data records.

        Yields
        ------
        dict
            Parsed row data from IXF file.
        """
        # Start parsing
        while not self.end_data_records:
            # Extract data
            self.current_row = self.collect_data()

            # Do not accept empty dictionary
            if not self.current_row:
                self.number_corrupted_rows += 1
                continue

            # Increment number of rows and yield the current row
            self.number_rows += 1

            yield self.current_row

    def parse(self) -> Iterable[Dict]:
        """Parse and yield a row.

        Returns
        -------
        Iterator[dict]:
            List of dictionaries containing parsed rows.
        """
        logger.debug("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()
        logger.debug("Get pyarrow schema")
        self.pyarrow_schema = get_pyarrow_schema(self.columns_info)

        logger.debug("Parse data records")
        for r in self.parse_data():
            yield r
        logger.debug("Finished parsing")

    def to_json(self, output: Union[str, Path, PathLike, TextIO]) -> bool:
        """Parse and convert to JSON.

        Parameters
        ----------
        output : Union[str, Path, PathLike, IO]
            Output file. It is better to use file-like object.

        Returns
        -------
        bool
            True if the parsing and conversion are ok.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode="w", encoding="utf-8")

        if not hasattr(output, "mode"):
            msg = "File-like object should have `mode` attribute"
            raise TypeError(msg)

        if output.mode not in ["w", "wt"]:
            msg = "File-like object should be opened in write and text mode"
            raise ValueError(msg)

        # Force utf-8 encoding for the json file
        # (Maybe we will need to log without forcing)
        if output.encoding != "utf-8":
            raise ValueError("File-like object should be `utf-8` encoded")

        logger.debug("Start writing in the json file")
        with output as out:
            out.write("[")
            first_row = True
            for r in self.parse():
                if not first_row:
                    out.write(",")
                json.dump(r, out, ensure_ascii=False, cls=CustomJSONEncoder)
                first_row = False
            out.write("]")
        logger.debug("Finished writing json file")

        total_rows = self.number_corrupted_rows + self.number_rows
        if total_rows == 0:
            logger.warning("Empty ixf file")
            return True

        logger.debug(f"Number of total rows = {total_rows}")
        logger.debug(f"Number of healthy rows = {self.number_rows}")
        logger.debug(f"Number of corrupted rows = {self.number_corrupted_rows}")

        cor_rate = self.number_corrupted_rows / total_rows * 100

        if int(cor_rate) != 0:
            logger.warning(f"Corrupted ixf file (rate={cor_rate}%)")

        if int(cor_rate) > DB2IXF_ACCEPTED_CORRUPTION_RATE:
            _msg = f"Corrupted data ({cor_rate}%) > ({DB2IXF_ACCEPTED_CORRUPTION_RATE}%)" \
                   f" accepted rate"
            logger.error(_msg)
            logger.warning(
                "You can change the accepted rate of the corrupted data by setting "
                "`DB2IXF_ACCEPTED_CORRUPTION_RATE` environment variable to a higher "
                "value"
            )
            raise IXFParsingError(_msg)

        return True

    # def to_jsonline(self, output: Union[str, Path, PathLike, TextIO]) -> bool:
    #     """Parse and convert to JSON Line Object.
    #
    #     Parameters
    #     ----------
    #     output : Union[str, Path, PathLike, IO]
    #         Output file. It is better to use file-like object.
    #
    #     Returns
    #     -------
    #     bool
    #         True if the parsing and conversion are ok.
    #     """
    #     if isinstance(output, (str, Path, PathLike)):
    #         output = open(output, mode="w", encoding="utf-8")
    #
    #     if not hasattr(output, "mode"):
    #         msg = "File-like object should have `mode` attribute"
    #         raise TypeError(msg)
    #
    #     if output.mode not in ["w", "wt"]:
    #         msg = "File-like object should be opened in write and text mode"
    #         raise ValueError(msg)
    #
    #     # Force utf-8 encoding for the json file
    #     # (Maybe we will need to log without forcing)
    #     if output.encoding != "utf-8":
    #         raise ValueError("File-like object should be `utf-8` encoded")
    #
    #     logger.debug("Start writing in the json line file")
    #     with output as out:
    #         for r in self.parse():
    #             json.dump(r, out, ensure_ascii=False, cls=CustomJSONEncoder)
    #             out.write("\n")
    #     logger.debug("Finished writing json line file")
    #
    #     total_rows = self.number_corrupted_rows + self.number_rows
    #     if total_rows == 0:
    #         logger.warning("Empty ixf file")
    #         return True
    #
    #     logger.debug(f"Number of total rows = {total_rows}")
    #     logger.debug(f"Number of healthy rows = {self.number_rows}")
    #     logger.debug(f"Number of corrupted rows = {self.number_corrupted_rows}")
    #
    #     cor_rate = self.number_corrupted_rows / total_rows * 100
    #
    #     if int(cor_rate) != 0:
    #         logger.warning(f"Corrupted ixf file (rate={cor_rate}%)")
    #
    #     if int(cor_rate) > DB2IXF_ACCEPTED_CORRUPTION_RATE:
    #         _msg = f"Corrupted data ({cor_rate}%) > ({DB2IXF_ACCEPTED_CORRUPTION_RATE}%)" \
    #                f" accepted rate"
    #         logger.error(_msg)
    #         logger.warning(
    #             "You can change the accepted rate of the corrupted data by setting "
    #             "`DB2IXF_ACCEPTED_CORRUPTION_RATE` environment variable to a higher "
    #             "value"
    #         )
    #         raise IXFParsingError(_msg)
    #
    #     return True

    def to_csv(self, output: Union[str, Path, PathLike, TextIO], sep: str = "|") -> bool:
        """Parse and convert to CSV.

        Parameters
        ----------
        output : Union[str, Path, PathLike, TextIO]
            Output file. It is better to use file-like object.
        sep : str
            Separator/delimiter of the columns. It defaults to `|`.

        Returns
        -------
        bool
            True if the parsing and conversion are ok.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode="w", encoding="utf-8")

        if not hasattr(output, "mode"):
            raise TypeError("File-like object should have `mode` attribute")

        if output.mode not in ["w", "wt"]:
            msg = "File-like object should be opened in write and text mode"
            raise ValueError(msg)

        # Force utf-8 encoding for the csv file
        # (Maybe we only need to log without forcing)
        if output.encoding != "utf-8":
            raise ValueError("File-like object should be `utf-8` encoded")

        logger.debug("Start writing in the csv file")
        with output as out:
            writer = csv.writer(out, delimiter=sep)
            cols = [
                str(
                    c["IXFCNAME"], encoding="utf-8"
                ).strip() for c in self.columns_info
            ]
            writer.writerow(cols)
            for r in self.parse():
                writer.writerow(r.values())
        logger.debug("Finished writing csv file")

        total_rows = self.number_corrupted_rows + self.number_rows
        if total_rows == 0:
            logger.warning("Empty ixf file")
            return True

        logger.debug(f"Number of total rows = {total_rows}")
        logger.debug(f"Number of healthy rows = {self.number_rows}")
        logger.debug(f"Number of corrupted rows = {self.number_corrupted_rows}")

        cor_rate = self.number_corrupted_rows / total_rows * 100

        if int(cor_rate) != 0:
            logger.warning(f"Corrupted ixf file (rate={cor_rate}%)")

        if int(cor_rate) > DB2IXF_ACCEPTED_CORRUPTION_RATE:
            _msg = f"Corrupted data ({cor_rate}%) > ({DB2IXF_ACCEPTED_CORRUPTION_RATE}%)" \
                   f" accepted rate"
            logger.error(_msg)
            logger.warning(
                "You can change the accepted rate of the corrupted data by setting "
                "`DB2IXF_ACCEPTED_CORRUPTION_RATE` environment variable to a higher "
                "value"
            )
            raise IXFParsingError(_msg)

        return True

    def to_parquet(
        self,
        output: Union[str, Path, PathLike, BinaryIO],
        batch_size: int = 10000,
        parquet_version: str = "2.4"
    ) -> bool:
        """Parse and convert to parquet.

        Parameters
        ----------
        output : Union[str, Path, PathLike, BinaryIO]
            Output file. It is better to use file-like object.
        batch_size : int
            Number of rows to extract before writing to the parquet file.
            It is used for memory optimization.
        parquet_version : str
            Parquet version. Please look at pyarrow documentation.

        Returns
        -------
        bool:
            True if the parsing and conversion are ok.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode="wb")

        if not hasattr(output, "mode"):
            raise TypeError("File-like object should have `mode` attribute")

        # Accept only write and text mode when opening output file
        if output.mode != "wb":
            msg = "File-like object should be opened in write and binary mode"
            raise ValueError(msg)

        logger.debug("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()
        logger.debug("Get pyarrow schema")
        self.pyarrow_schema = get_pyarrow_schema(self.columns_info)

        logger.debug("Start writing in the parquet file")
        with output as of:
            with ParquetWriter(
                    where=of,
                    schema=self.pyarrow_schema,
                    flavor="spark",
                    version=parquet_version
            ) as writer:
                record_batches = pyarrow_record_batches(
                    self.parse_data(),
                    self.pyarrow_schema,
                    batch_size
                )
                for batch in record_batches:
                    writer.write_batch(batch)
        logger.debug("Finished writing parquet file")

        total_rows = self.number_corrupted_rows + self.number_rows
        if total_rows == 0:
            logger.warning("Empty ixf file")
            return True

        logger.debug(f"Number of total rows = {total_rows}")
        logger.debug(f"Number of healthy rows = {self.number_rows}")
        logger.debug(f"Number of corrupted rows = {self.number_corrupted_rows}")

        cor_rate = self.number_corrupted_rows / total_rows * 100

        if int(cor_rate) != 0:
            logger.warning(f"Corrupted ixf file (rate={cor_rate}%)")

        if int(cor_rate) > DB2IXF_ACCEPTED_CORRUPTION_RATE:
            _msg = f"Corrupted data ({cor_rate}%) > ({DB2IXF_ACCEPTED_CORRUPTION_RATE}%)" \
                   f" accepted rate"
            logger.error(_msg)
            logger.warning(
                "You can change the accepted rate of the corrupted data by setting "
                "`DB2IXF_ACCEPTED_CORRUPTION_RATE` environment variable to a higher "
                "value"
            )
            raise IXFParsingError(_msg)

        return True

    def to_deltalake(
        self,
        table_or_uri: Union[str, Path, DeltaTable],
        partition_by: Optional[Union[List[str], str]] = None,
        mode: Literal["error", "append", "overwrite", "ignore"] = "error",
        overwrite_schema: bool = False,
        partition_filters: Optional[List[Tuple[str, str, Any]]] = None,
        large_dtypes: bool = False,
        batch_size: int = 10000,
        **kwargs
    ) -> bool:
        """Parse and convert to a deltalake table.

        Parameters
        ----------
        table_or_uri : Union[str, pathlib.Path, DeltaTable]
            URI of a table or a DeltaTable object.
        partition_by : Optional[Union[List[str], str]]
            List of columns to partition the table by. Only required when
            creating a new table.
        mode : Literal["error", "append", "overwrite", "ignore"]
            How to handle existing data.
            Default is to error if table already exists.
                If "append", will add new data.
                If "overwrite", will replace table with new data.
                If "ignore", will not write anything if table already exists.
        overwrite_schema : bool
            If True, allows updating the schema of the table.
        partition_filters : Optional[List[Tuple[str, str, Any]]]
            Defaults to None. The partition filters that will be used for
            partition overwrite. Only used in pyarrow engine.
        large_dtypes : bool
            If True, the table schema is checked against large_dtypes.
        batch_size : int
            Number of rows to extract before conversion operation.
            If None, the number of rows will be equal to 100000. It is used for
            memory optimization.
        **kwargs : Optional[dict]
            Some of the arguments you can give to this function
            `deltalake.write_deltalake`. See doc in
            https://delta-io.github.io/delta-rs/python/api_reference.html#writing-deltatables.
            Please, do not duplicate with the ones used in this function.

        Returns
        -------
        bool:
            True if the parsing and conversion are ok.
        """
        logger.debug("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()
        logger.debug("Get pyarrow schema")
        self.pyarrow_schema = get_pyarrow_schema(self.columns_info)

        logger.debug("Apply fixes on pyarrow schema for deltalake adaptation")
        fixed_schema = apply_schema_fixes(self.pyarrow_schema)

        logger.debug("Start writing to deltalake")
        data = iter(pyarrow_record_batches(iter(self.parse_data()), fixed_schema, batch_size))
        deltalake.write_deltalake(
            table_or_uri=table_or_uri,
            data=data,
            schema=fixed_schema,
            partition_by=partition_by,
            mode=mode,
            overwrite_schema=overwrite_schema,
            partition_filters=partition_filters,
            large_dtypes=large_dtypes,
            **kwargs
        )
        logger.debug("End writing to deltalake")

        total_rows = self.number_corrupted_rows + self.number_rows
        if total_rows == 0:
            logger.warning("Empty ixf file")
            return True

        logger.debug(f"Number of total rows = {total_rows}")
        logger.debug(f"Number of healthy rows = {self.number_rows}")
        logger.debug(f"Number of corrupted rows = {self.number_corrupted_rows}")

        cor_rate = self.number_corrupted_rows / total_rows * 100

        if int(cor_rate) != 0:
            logger.warning(f"Corrupted ixf file (rate={cor_rate}%)")

        if int(cor_rate) > DB2IXF_ACCEPTED_CORRUPTION_RATE:
            _msg = f"Corrupted data ({cor_rate}%) > ({DB2IXF_ACCEPTED_CORRUPTION_RATE}%)" \
                   f" accepted rate"
            logger.error(_msg)
            logger.warning(
                "You can change the accepted rate of the corrupted data by setting "
                "`DB2IXF_ACCEPTED_CORRUPTION_RATE` environment variable to a higher "
                "value"
            )
            raise IXFParsingError(_msg)

        return True


__all__ = ["IXFParser"]
