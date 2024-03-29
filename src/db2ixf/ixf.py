# coding=utf-8
"""Creates an PC/IXF parser"""
from __future__ import annotations

import sys

import csv
import deltalake
import json
from collections import OrderedDict, defaultdict
from db2ixf.collectors import collectors
from db2ixf.constants import (
    COL_DESCRIPTOR_RECORD_TYPE, DATA_RECORD_TYPE,
    DB2IXF_ACCEPTED_CORRUPTION_RATE, HEADER_RECORD_TYPE,
    TABLE_RECORD_TYPE,
)
from db2ixf.encoders import CustomJSONEncoder
from db2ixf.exceptions import (
    DataCollectorError, IXFParsingError, NotValidColumnDescriptorException,
    UnknownDataTypeException,
)
from db2ixf.helpers import (
    apply_schema_fixes, deprecated, get_column_names, get_filesize,
    get_opt_batch_size, get_pyarrow_schema,
    init_opt_batch_size, to_pyarrow_record_batch,
)
from db2ixf.logger import logger
from deltalake import DeltaTable
from os import PathLike
from pathlib import Path
from pyarrow import RecordBatch, Schema, schema
from pyarrow.parquet import ParquetWriter
from typing import (
    Any, BinaryIO, Dict, Iterable, List, Literal, Optional, TextIO,
    Tuple, Union,
)


class IXFParser:
    """PC/IXF Parser.

    Attributes
    ----------
    file : str, Path, PathLike or File-Like Object
        Input file and it is better to use file-like object.
    """

    def __init__(self, file: Union[str, Path, PathLike, BinaryIO]):
        """Init an instance of the PC/IXF Parser.

        Parameters
        ----------
        file : str, Path, PathLike or File-Like Object
            Input file and it is better to use file-like object.
        """
        if isinstance(file, (str, Path, PathLike)):
            file = open(file, mode="rb")
            logger.debug("File opened in read & binary mode")

        if file.mode != "rb":
            msg = "file-like object should be opened in read-binary mode"
            raise ValueError(msg)

        # Init instance attributes
        self.file = file

        # State
        self.file_size: int = get_filesize(file)
        logger.debug(f"File size = {self.file_size} bytes")
        """IXF file size"""
        self.header_record: OrderedDict = OrderedDict()
        """Contains header metadata extracted from the ixf file."""
        self.table_record: OrderedDict = OrderedDict()
        """Contains table metadata extracted from the ixf file."""
        self.column_records: List[OrderedDict] = []
        """Contains columns description extracted from the ixf file."""
        self.pyarrow_schema: Schema = schema([])
        """Pyarrow schema extracted from the ixf file."""
        self.current_data_record: OrderedDict = OrderedDict()
        """Contains current data record extracted from ixf file."""
        self.end_data_records: bool = False
        """Flag the end of the data records in the ixf file."""
        self.current_row: OrderedDict = OrderedDict()
        """Contains parsed data extracted from a data record of the ixf file."""
        self.current_row_size: int = 0
        """Current row size in bytes"""
        self.current_total_size: int = 0
        """Current total size of the rows"""
        self.number_rows: int = 0
        """Number of rows extracted from the ixf file."""
        # Avoids counting the last line (EOF)
        self.number_corrupted_rows: int = -1
        """Number of corrupted rows in the ixf file."""
        self.opt_batch_size: int = init_opt_batch_size(self.file_size)
        """Estimated optimal batch size"""

    def __read_header(
        self,
        record_type: OrderedDict = None
    ) -> OrderedDict:
        """Read the header record.

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
            self.header_record[u] = self.file.read(w)

        return self.header_record

    def __read_table(
        self,
        record_type: OrderedDict = None
    ) -> OrderedDict:
        """Read the table record.

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
            self.table_record[m] = self.file.read(n)

        return self.table_record

    def __read_column_records(
        self,
        record_type: OrderedDict = None
    ) -> List[OrderedDict]:
        """Read the column records.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Returns
        -------
        List[OrderedDict]
            Column descriptors records of the input file.

        Raises
        ------
        NotValidColumnDescriptorException
            If the IXF contains a non valid column descriptor.
        """
        if record_type is None:
            record_type = COL_DESCRIPTOR_RECORD_TYPE

        # "IXFTCCNT" contains number of columns in the table
        for _ in range(0, int(self.table_record["IXFTCCNT"])):
            column = OrderedDict()
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

            self.column_records.append(column)

        return self.column_records

    def __read_data_record(
        self,
        record_type: OrderedDict = None
    ) -> OrderedDict:
        """Read one data record.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Returns
        ------
        OrderedDict
            Dictionary containing current data record from IXF file.
        """
        if record_type is None:
            record_type = DATA_RECORD_TYPE

        self.current_data_record = OrderedDict()
        for key, val in record_type.items():
            self.current_data_record[key] = self.file.read(val)

        self.current_data_record["IXFDCOLS"] = self.file.read(
            int(self.current_data_record["IXFDRECL"]) - 8
        )
        return self.current_data_record

    def __parse_data_record(self) -> OrderedDict:
        """Parses one data record.

        It collects data from fields of the current data record.

        Returns
        -------
        OrderedDict:
            Dictionary containing all extracted data from fields of
            the data record.
        """
        # Start Extraction
        try:
            self.current_row = OrderedDict()
            for c in self.column_records:
                # Extract some metadata about the column
                col_name = str(c["IXFCNAME"], encoding="utf-8").strip()
                col_type = int(c["IXFCTYPE"])
                col_is_nullable = c["IXFCNULL"] == b"Y"
                col_position = int(c["IXFCPOSN"])

                # Init the data collection
                self.current_row[col_name] = None
                collected_data = None  # noqa

                # Parse next data record in case a column is in position 1
                if col_position == 1:
                    self.__read_data_record()

                # Mark the end of data records: helps exit the while loop
                if self.current_data_record["IXFDRECT"] != b"D":
                    self.end_data_records = True
                    self.current_row = OrderedDict()
                    logger.debug("End of data records")
                    break

                # Position index is then equals to position - 1
                pos = col_position - 1

                # Handle nullable
                if col_is_nullable:
                    # Column is null
                    _dr = self.current_data_record["IXFDCOLS"][pos:pos + 2]
                    if _dr == b"\xff\xff":
                        self.current_row[col_name] = None
                        continue
                    # Column is not null
                    elif _dr == b"\x00\x00":
                        pos += 2

                # Collect data
                collector = collectors.get(col_type, None)
                if collector is None:
                    msg = f"The column {col_name} has unknown " \
                          f"data type {col_type}"
                    raise UnknownDataTypeException(msg)

                collected_data = collector(
                    c, self.current_data_record["IXFDCOLS"], pos
                )
                self.current_row[col_name] = collected_data

            self.current_data_record = OrderedDict()
            return self.current_row
        except DataCollectorError as er1:
            logger.error(er1)
            self.current_row = OrderedDict()
            return self.current_row
        except (UnknownDataTypeException, Exception) as er2:
            logger.error(er2)
            self.current_row = OrderedDict()
            raise IXFParsingError(er2)

    def __update_statistics(self) -> "IXFParser":
        """Update stats and change state of the parser"""
        # Stats calculation
        self.number_rows += 1
        self.current_row_size = sys.getsizeof(self.current_row)
        self.current_total_size += self.current_row_size
        if self.number_rows == 0:
            self.estimated_row_size = self.current_row_size
        else:
            self.estimated_row_size = self.current_total_size \
                                      / self.number_rows

        self.opt_batch_size = get_opt_batch_size(
            self.opt_batch_size,
            self.estimated_row_size
        )

        return self

    def __parse_all_data_records(self) -> Iterable[OrderedDict]:
        """Parses all the data records.

        Yields
        ------
        dict
            Parsed row data from IXF file.
        """
        # Start parsing
        while not self.end_data_records:
            # Extract data
            self.__parse_data_record()

            # Do not accept empty dictionary
            if not self.current_row:
                self.number_corrupted_rows += 1
                continue

            self.__update_statistics()
            yield self.current_row

    def __start_parsing(self) -> "IXFParser":
        """Starts the parsing."""
        logger.debug("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.__read_header()
        logger.debug("Parse table record")
        self.__read_table()
        logger.debug("Parse column descriptor records")
        self.__read_column_records()
        return self

    def start_parsing(self) -> "IXFParser":
        """Starts the parsing."""
        return self.__start_parsing()

    def __check_parsing(self) -> bool:
        """Do some checks on the parsing."""
        total_rows = self.number_corrupted_rows + self.number_rows
        if total_rows == 0:
            logger.warning("Empty ixf file")
            self.file.close()
            return True

        logger.debug(f"Number of total rows = {total_rows}")
        logger.debug(f"Number of healthy rows = {self.number_rows}")
        logger.debug(f"Number of corrupted rows = {self.number_corrupted_rows}")

        cor_rate = self.number_corrupted_rows / total_rows * 100

        if int(cor_rate) != 0:
            logger.warning(f"Corrupted ixf file (rate={cor_rate}%)")

        if int(cor_rate) > DB2IXF_ACCEPTED_CORRUPTION_RATE:
            _msg = f"Corrupted data ({cor_rate}%) > " \
                   f"({DB2IXF_ACCEPTED_CORRUPTION_RATE}%) accepted rate"
            logger.error(_msg)
            logger.warning(
                "You can change the accepted rate of the corrupted data "
                "by setting `DB2IXF_ACCEPTED_CORRUPTION_RATE` environment "
                "variable to a higher value"
            )
            self.file.close()
            raise IXFParsingError(_msg)

        self.file.close()
        return True

    def check_parsing(self) -> bool:
        """Do some checks on the parsing.

        Returns
        -------
        bool
            True if parsing and/or conversion are ok.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        return self.__check_parsing()

    def __iter_row(self) -> Iterable[Dict]:
        """Yields extracted rows (Without parsing of header, table, cols)."""
        logger.debug("Parse all data records")
        for r in self.__parse_all_data_records():
            yield dict(r)
        logger.debug("Finished parsing")

    def iter_row(self) -> Iterable[Dict]:
        """Yields parsed rows.

        It won't work if you use it alone. you need to start parsing with
        `start_parsing` method then you can iterate over rows using `iter_row`.
        Most of the time, you do not need to use this method.

        You will need it in case you want to customize the parsing for
        example adding support for a new output format.
        """
        return self.__iter_row()

    def __iter_batch_of_rows(
        self,
        data: Optional[Iterable[Dict]] = None,
        batch_size: Optional[int] = None
    ) -> Iterable[List[Dict]]:
        """Yields batch of parsed rows."""
        if data is None:
            data = self.__iter_row()

        if not isinstance(data, Iterable):
            raise TypeError(f"Expecting an `Iterable`, Got: {type(data)}")

        if batch_size is None:
            _size = self.opt_batch_size
        else:
            _size = batch_size

        if not isinstance(_size, int):
            TypeError(f"Expecting an `Integer`, Got {type(_size)}")

        batch = []
        counter = 0
        for i, row in enumerate(data):
            batch.append(row)
            counter += 1
            if counter % _size == 0:
                _size = batch_size if batch_size else self.opt_batch_size
                yield batch
                batch = []

        # Yield the remaining rows as the last batch
        if batch:
            yield batch

    def iter_batch_of_rows(
        self,
        data: Optional[Iterable[Dict]] = None,
        batch_size: Optional[int] = None
    ) -> Iterable[List[Dict]]:
        """Yields batches of parsed rows.

        It won't work if you use it alone. you need to start parsing with
        `start_parsing` method then you can iterate over batch of rows using
        `iter_batch_of_rows` method. Most of the time, you do not need to use
        this method.

        You will need it in case you want to customize the parsing for
        example adding support for a new output format.

        Parameters
        ----------
        data : Iterable[Dict]
            Data extracted from ixf file (parsed rows).
        batch_size : int
            Batch size.

        Yields
        ------
        List[Dict]
            Batch of 

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        batches = self.__iter_batch_of_rows(
            data=data,
            batch_size=batch_size
        )
        for batch in batches:
            yield batch

    def __iter_pyarrow_record_batch(
        self,
        data: Optional[Iterable[Dict]] = None,
        batch_size: Optional[int] = None,
    ) -> Iterable[RecordBatch]:
        """Yields pyarrow record batches from an iterable of rows."""
        if data is None:
            data = self.__iter_row()

        if not isinstance(data, Iterable):
            raise TypeError(f"Expecting an `Iterable`, Got: {type(data)}")

        if batch_size is None:
            _size = self.opt_batch_size
        else:
            _size = batch_size

        if not isinstance(_size, int):
            TypeError(f"Expecting an `Integer`, Got {type(_size)}")

        batch = defaultdict(list)
        counter = 0
        for i, row in enumerate(data):
            for key, value in row.items():
                batch[key].append(value)
            counter += 1
            if counter % _size == 0:
                _size = batch_size if batch_size else self.opt_batch_size
                yield to_pyarrow_record_batch(batch, self.pyarrow_schema)
                batch = defaultdict(list)

        if batch:
            yield to_pyarrow_record_batch(batch, self.pyarrow_schema)
            batch.clear()

    def iter_pyarrow_record_batch(
        self,
        data: Optional[Iterable[Dict]] = None,
        batch_size: Optional[int] = None,
    ) -> Iterable[RecordBatch]:
        """Yields pyarrow record batches.

        It won't work if you use it alone. you need to start parsing with
        `start_parsing` method, create the pyarrow schema using
        `get_or_create_pyarrow_schema` method then you can iterate over record
        batches using `iter_batch_of_rows` method. Most of the time, you do not
        need to use this method.

        You will need it in case you want to customize the parsing for
        example adding support for a new output format.

        Parameters
        ----------
        data : Iterable[Dict]
            Data extracted from ixf file (parsed rows).
        batch_size : int
            Batch size.

        Yields
        ------
        RecordBatch
            Pyarrow record batch.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        batches = self.__iter_pyarrow_record_batch(
            data=data,
            batch_size=batch_size,
        )

        for batch in batches:
            yield batch

    def __get_or_create_pyarrow_schema(
        self,
        pyarrow_schema: Optional[Schema] = None,
        for_delta: Optional[bool] = False
    ) -> Schema:
        """Get or create pyarrow schema based on the scope it will be used."""
        if pyarrow_schema is None:
            logger.debug("Get pyarrow schema from column records")
            pyarrow_schema = get_pyarrow_schema(self.column_records)

        if for_delta:
            logger.debug(
                "Apply fixes on pyarrow schema for deltalake adaptation"
            )
            pyarrow_schema = apply_schema_fixes(pyarrow_schema)

        self.pyarrow_schema = pyarrow_schema

        return self.pyarrow_schema

    def get_or_create_pyarrow_schema(
        self,
        pyarrow_schema: Optional[Schema] = None,
        for_delta: Optional[bool] = False
    ) -> Schema:
        """Get or create pyarrow schema based on the scope of the usage.

        It won't work if you use it alone. you need to start parsing with
        `start_parsing` method then you can create the pyarrow schema using
        `get_or_create_pyarrow_schema` method. After applying it, you will maybe
        need to iterate over pyarrow record batches. Most of the time, you do
        not need to use this method.

        You will need it in case you want to customize the parsing for
        example adding support for a new output format.

        Parameters
        ----------
        pyarrow_schema : Schema
            Pyarrow schema.
        for_delta : bool
            If True, it adapts pyarrow schema for deltalake usage.

        Returns
        -------
        Schema
            Pyarrow schema
        """
        _schema = self.__get_or_create_pyarrow_schema(
            pyarrow_schema=pyarrow_schema,
            for_delta=for_delta
        )
        return _schema

    def get_row(self) -> Iterable[Dict]:
        """Yields parsed rows.

        Yields
        ------
        Dict
            Generated parsed row.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        self.__start_parsing()
        for r in self.__iter_row():
            yield r

    @deprecated("0.16.0", "Use `get_row` method instead of `parse`.")
    def parse(self) -> Iterable[Dict]:
        """Yields parsed rows.

        Alias for `get_row` for compatibility with old versions.

        Yields
        ------
        Dict
            Generated parsed row.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        return self.get_row()

    def get_all_rows(self) -> List[Dict]:
        """Get all the parsed rows from the ixf file.

        Returns
        -------
        List[Dict]
            List of all extracted rows.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.

        Notes
        -----
        - Attention: it loads all the extracted rows into memory.
        """
        rows = []
        for row in self.get_row():
            rows.append(row)

        if self.__check_parsing() is True:
            return rows
        return rows

    def to_json(
        self,
        output: Union[str, Path, PathLike, TextIO]
    ) -> bool:
        """Parses and converts to JSON format.

        Parameters
        ----------
        output : Union[str, Path, PathLike, IO]
            Output file. It is better to use file-like object.

        Returns
        -------
        bool
            True if the parsing and conversion are ok.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
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

        # init the parsing
        self.__start_parsing()
        _rows = self.__iter_row()

        logger.debug("Start writing in the json file")
        with output as out:
            out.write("[")
            first_row = True
            for r in _rows:
                if not first_row:
                    out.write(",")
                json.dump(r, out, ensure_ascii=False, cls=CustomJSONEncoder)
                first_row = False
            out.write("]")
        logger.debug("Finished writing json file")

        # dereference source data
        del _rows

        return self.__check_parsing()

    def to_jsonline(
        self,
        output: Union[str, Path, PathLike, TextIO]
    ) -> bool:
        """Parses and converts to JSON LINE format.

        Parameters
        ----------
        output : Union[str, Path, PathLike, IO]
            Output file. It is better to use file-like object.

        Returns
        -------
        bool
            True if the parsing and conversion are ok.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
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

        # init the parsing
        self.__start_parsing()
        _rows = self.__iter_row()

        logger.debug("Start writing in the json line file")
        with output as out:
            for r in _rows:
                json.dump(r, out, ensure_ascii=False, cls=CustomJSONEncoder)
                out.write("\n")
        logger.debug("Finished writing json line file")

        # dereference source data
        del _rows

        return self.__check_parsing()

    def to_csv(
        self,
        output: Union[str, Path, PathLike, TextIO],
        sep: Optional[str] = "|",
        batch_size: Optional[int] = None
    ) -> bool:
        """Parses and converts to CSV format.

        Parameters
        ----------
        output : Union[str, Path, PathLike, TextIO]
            Output file. It is better to use file-like object
        sep : str
            Separator/delimiter of the columns.
        batch_size : int
            Batch size, it used for memory optimization

        Returns
        -------
        bool
            True if the parsing and conversion are ok

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
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

        # init the parsing
        self.__start_parsing()
        batches = self.__iter_batch_of_rows(batch_size=batch_size)

        logger.debug("Start writing in the csv file")
        with output as out:
            writer = csv.writer(out, delimiter=sep)
            writer.writerow(get_column_names(self.column_records))
            for rows in batches:
                writer.writerows([r.values() for r in rows])
        logger.debug("Finished writing csv file")

        # dereference source data
        del batches

        return self.__check_parsing()

    def get_pyarrow_record_batch(
        self,
        data: Optional[Iterable[Dict]] = None,
        batch_size: Optional[int] = None,
        for_delta: Optional[bool] = False
    ) -> Iterable[RecordBatch]:
        """Yields pyarrow records batches.

        Parameters
        ----------
        data : Iterable[Dict]
            Data extracted from ixf file (parsed rows).
        batch_size : int
            Batch size.
        for_delta : bool
            If True, it adapts pyarrow schema for deltalake usage.

        Yields
        ------
        RecordBatch
            Pyarrow record batch.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        self.__start_parsing()
        self.pyarrow_schema = self.__get_or_create_pyarrow_schema(
            for_delta=for_delta
        )
        batches = self.__iter_pyarrow_record_batch(
            data=data,
            batch_size=batch_size,
        )
        for batch in batches:
            yield batch

    def to_parquet(
        self,
        output: Union[str, Path, PathLike, BinaryIO],
        parquet_version: str = "2.6",
        batch_size: int = None
    ) -> bool:
        """Parses and converts to PARQUET format.

        Parameters
        ----------
        output : Union[str, Path, PathLike, BinaryIO]
            Output file. It is better to use file-like object.
        parquet_version : str
            Parquet version. Please see pyarrow documentation.
        batch_size : int
            Number of rows to extract before writing to the parquet file.
            It is used for memory optimization.

        Returns
        -------
        bool
            True if the parsing and conversion are ok.

        Raises
        ------
        IXFParsingError
            In case it encounters a parsing error.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode="wb")

        if not hasattr(output, "mode"):
            raise TypeError("File-like object should have `mode` attribute")

        # Accept only write and text mode when opening output file
        if output.mode != "wb":
            msg = "File-like object should be opened in write and binary mode"
            raise ValueError(msg)

        # Init the parsing
        self.__start_parsing()
        self.pyarrow_schema = self.__get_or_create_pyarrow_schema()
        batches = self.__iter_pyarrow_record_batch(batch_size=batch_size)

        logger.debug("Start writing parquet file")
        with output as of:
            with ParquetWriter(
                    where=of,
                    schema=self.pyarrow_schema,
                    flavor="spark",
                    version=parquet_version
            ) as writer:
                for batch in batches:
                    writer.write_batch(batch)
        logger.debug("Finished writing parquet file")

        # dereference source data
        del batches

        return self.__check_parsing()

    def to_deltalake(
        self,
        table_or_uri: Union[str, Path, DeltaTable],
        partition_by: Optional[Union[List[str], str]] = None,
        mode: Literal["error", "append", "overwrite", "ignore"] = "error",
        overwrite_schema: bool = False,
        schema_mode: Optional[Literal["merge", "overwrite"]] = None,
        partition_filters: Optional[List[Tuple[str, str, Any]]] = None,
        large_dtypes: bool = False,
        batch_size: Optional[int] = None,
        **kwargs
    ) -> bool:
        """Parses and converts to a deltalake table.

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
        schema_mode : Optional[Literal["merge", "overwrite"]]
            If set to "overwrite", allows replacing the schema of the table.
            Set to "merge" to merge with existing schema.
        partition_filters : Optional[List[Tuple[str, str, Any]]]
            Defaults to None. The partition filters that will be used for
            partition overwrite. Only used in pyarrow engine.
        large_dtypes : bool
            If True, the table schema is checked against large_dtypes.
        batch_size : int
            Number of rows to extract before conversion operation.
            It is used for memory optimization.
        **kwargs : Optional[dict]
            Some of the arguments you can give to this function
            `deltalake.write_deltalake`. See doc in
            https://delta-io.github.io/delta-rs/python/api_reference.html.
            Please, do not duplicate with the ones used in this function.

        Returns
        -------
        bool:
            True if the parsing and conversion are ok.
        """
        # Init the parsing
        self.__start_parsing()
        self.pyarrow_schema = self.__get_or_create_pyarrow_schema(
            for_delta=True
        )
        batches = self.__iter_pyarrow_record_batch(batch_size=batch_size)

        logger.debug("Start writing to deltalake")
        deltalake.write_deltalake(
            table_or_uri=table_or_uri,
            data=batches,
            schema=self.pyarrow_schema,
            partition_by=partition_by,
            mode=mode,
            overwrite_schema=overwrite_schema,
            schema_mode=schema_mode,
            partition_filters=partition_filters,
            large_dtypes=large_dtypes,
            **kwargs
        )
        logger.debug("Finished writing to deltalake")

        # dereference source data
        del batches

        return self.__check_parsing()


__all__ = ["IXFParser"]
