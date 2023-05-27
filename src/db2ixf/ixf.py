# coding=utf-8
"""Creates an PC/IXF parser"""
from __future__ import annotations

import sys

import csv
import json
import pyarrow.parquet
from db2ixf.collectors import (collect_bigint,
                                                     collect_char,
                                                     collect_date,
                                                     collect_decimal,
                                                     collect_integer,
                                                     collect_time,
                                                     collect_timestamp,
                                                     collect_varchar,
                                                     collect_smallint)
from db2ixf.constants import (HEADER_RECORD_TYPE,
                                                    TABLE_RECORD_TYPE,
                                                    COL_DESCRIPTOR_RECORD_TYPE,
                                                    DATA_RECORD_TYPE)
from db2ixf.encoders import CustomJSONEncoder
from db2ixf.exceptions import (
    NotValidColumnDescriptorException,
    UnknownDataTypeException)
from db2ixf.helpers import get_batch, get_pyarrow_schema
from db2ixf.logger import logger
from os import PathLike
from pathlib import Path
from pyarrow.parquet import ParquetWriter
from typing import Union, List, BinaryIO, TextIO


class IXFParser:
    """
    PC/IXF Parser.

    Attributes
    ----------
    file : str, Path, PathLike or File-Like Object
        Input file and it is better to use file-like object.
    encoding: str, default: latin-1
        Encoding of the ixf file. Defaults to latin-1 (ISO 8859-1).
    """
    header_info: dict
    """Contains header informations from input ixf file."""
    table_info: dict
    """Contains table informations from input ixf file."""
    columns_info: List[dict]
    """Contains columns description from input ixf file."""
    schema: dict
    """Schema extracted from metadata in the input ixf file."""
    current_data_record: dict
    """Contains current data record from input ixf file."""
    end_data_records: bool
    """Flag the end of data records in the input ixf file."""
    current_row: dict
    """Contains parsed data extracted from a data record of the input ixf 
    file."""
    number_rows: int
    """Number of rows extracted from the input ixf file."""

    def __init__(self,
                 file: Union[str, Path, PathLike, BinaryIO],
                 encoding: str = 'latin-1'):
        """Init the instance."""
        logger.debug('Start initializing the parser')

        if isinstance(file, (str, Path, PathLike)):
            file = open(file, mode='rb')
            logger.debug('File opened in read & binary mode')

        try:
            if file.mode != 'rb':
                msg = 'file-like object should be opened in ' \
                      'read and binary mode'
                raise ValueError(msg)
        except Exception as e:
            logger.error('Parser has an error while reading the ixf file')
            logger.error(e)
            sys.exit(1)  # Exit the program with a non-zero exit code

        # Init instance attributes
        self.file = file
        self.encoding = encoding

        # State
        self.header_info = {}
        self.table_info = {}
        self.columns_info = []
        self.schema = {}
        self.current_data_record = {}
        self.end_data_records = False
        self.current_row = {}
        self.number_rows = 0

        logger.info('Parser init finished')

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

        # 'IXFTCCNT' contains number of columns in the table
        for _ in range(0, int(self.table_info['IXFTCCNT'])):

            column = {}
            for i, j in record_type.items():
                column[i] = self.file.read(j)

            try:
                if column['IXFCRECT'] != b'C':
                    c = str(column['IXFCNAME'], encoding=self.encoding).strip()
                    msg = f'IXF file is not valid, it contains a not ' \
                          f'valid column descriptor (see {c}).'
                    raise NotValidColumnDescriptorException(msg)
            except Exception as e:
                logger.error(e)
                sys.exit(1)

            column['IXFCDSIZ'] = self.file.read(int(column['IXFCRECL']) - 862)
            self.columns_info.append(column)
        return self.columns_info

    def parse_data_record(self, record_type: dict = None):
        """Parse one data record.

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

        self.current_data_record['IXFDCOLS'] = self.file.read(
            int(self.current_data_record['IXFDRECL']) - 8
        )
        return self.current_data_record

    def extract_data(self) -> dict:
        """Extract data from fields of the current data record.

        Returns
        -------
        dict:
            Dictionary containing all extracted data from fields of
            the data record.
        """
        # Start Extraction
        r = {}
        for c in self.columns_info:
            col_name = str(c['IXFCNAME'], encoding=self.encoding).strip()
            col_type = int(c['IXFCTYPE'])
            col_is_nullable = c['IXFCNULL'] == b'Y'
            col_position = int(c['IXFCPOSN'])

            # Parse next data record in case a column is in position 1
            if col_position == 1:
                self.parse_data_record()

            # Mark the end of data records: helps exit the while loop
            if self.current_data_record['IXFDRECT'] != b'D':
                self.end_data_records = True
                logger.debug('End of data records')
                break

            # Position index is then equals to position - 1
            pos = col_position - 1

            # Handle nullable
            if col_is_nullable:
                # Column is null
                if self.current_data_record['IXFDCOLS'][
                   pos:pos + 2] == b'\xff\xff':
                    r[col_name] = None
                    continue
                # Column is not null
                elif self.current_data_record['IXFDCOLS'][
                     pos:pos + 2] == b'\x00\x00':
                    pos += 2

            # Collect data
            switcher = {
                384: collect_date,
                388: collect_time,
                392: collect_timestamp,
                448: collect_varchar,
                452: collect_char,
                484: collect_decimal,
                492: collect_bigint,
                496: collect_integer,
                500: collect_smallint,
            }
            func = switcher.get(col_type, None)
            try:
                if func is None:
                    msg = f'The column {col_name} has unknown data ' \
                          f'type {col_type}'
                    raise UnknownDataTypeException(msg)
                else:
                    r[col_name] = func(
                        c,
                        self.current_data_record['IXFDCOLS'],
                        pos,
                        self.encoding
                    )
            except Exception as e:
                logger.error(e)
                sys.exit(1)

        return r

    def parse_data(self, record_type: dict = None) -> dict:
        """Parse data records.

        Parameters
        ----------
        record_type : dict
            Dictionary containing the names of the record fields and
            their length.

        Yields
        ------
        dict
            Parsed row data from IXF file.
        """
        if record_type is None:
            record_type = DATA_RECORD_TYPE

        # Init the state
        self.number_rows = 0

        # Start parsing
        while not self.end_data_records:
            # Extract data
            self.current_row = {}
            self.current_row = self.extract_data()

            # Do not accept empty dictionary
            if not self.current_row:
                continue

            # Increment number of rows and yield the current row
            self.number_rows += 1

            yield self.current_row

    def parse(self) -> List[dict]:
        """Parse to a python list of dictionaries.

        Returns
        -------
        List[dict]:
            List of dictionaries containing parsed rows.
        """
        logger.info("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()

        logger.debug("Parse data records")
        rows = []
        for r in self.parse_data():
            rows.append(r)

        logger.info(f'Number of rows is: {self.number_rows}')
        logger.info("Finished parsing")

        return rows

    def to_json(self, output: Union[str, Path, PathLike, TextIO]) -> int:
        """Parse and convert to JSON.

        Parameters
        ----------
        output : Union[str, Path, PathLike, IO]
            Output file. It is better to use file-like object.

        Returns
        -------
        int:
            0 if the parsing and conversion are ok.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode='w', encoding='utf-8')

        try:
            if not hasattr(output, 'mode'):
                msg = 'File-like object should have `mode` attribute'
                raise TypeError(msg)

            if output.mode not in ['w', 'wt']:
                msg = 'File-like object should be opened in write and text mode'
                raise ValueError(msg)

            # Force utf-8 encoding for the json file
            # (Maybe we will need to log without forcing)
            if output.encoding != 'utf-8':
                raise ValueError('File-like object should be `utf-8` encoded')
        except Exception as e:
            logger.error(e)
            sys.exit(1)

        logger.info("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()

        logger.debug("Start writing in the json file")
        with output as out:
            out.write("[")
            first_row = True
            for r in self.parse_data():
                if not first_row:
                    out.write(",")
                json.dump(r, out, ensure_ascii=False, cls=CustomJSONEncoder)
                first_row = False
            out.write("]")

        logger.info(f'Number of rows is: {self.number_rows}')
        logger.info('Finished writing json file')

        return 0

    def to_csv(self,
               output: Union[str, Path, PathLike, TextIO],
               sep: str = '|') -> int:
        """Parse and convert to CSV.

        Parameters
        ----------
        output : Union[str, Path, PathLike, TextIO]
            Output file. It is better to use file-like object.
        sep : str
            Separator/delimiter of the columns. It defaults to `|`.

        Returns
        -------
        int:
            0 if the parsing and conversion are ok.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode='w', encoding='utf-8')

        try:
            if not hasattr(output, 'mode'):
                raise TypeError('File-like object should have `mode` attribute')

            if output.mode not in ['w', 'wt']:
                msg = 'File-like object should be opened in write and text mode'
                raise ValueError(msg)

            # Force utf-8 encoding for the csv file
            # (Maybe we only need to log without forcing)
            if output.encoding != 'utf-8':
                raise ValueError('File-like object should be `utf-8` encoded')
        except Exception as e:
            logger.error(e)
            sys.exit(1)

        logger.info("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()

        logger.debug("Start writing in the csv file")
        with output as out:
            writer = csv.writer(out, delimiter=sep)
            cols = [
                str(
                    c['IXFCNAME'],
                    encoding=self.encoding
                ).strip() for c in self.columns_info
            ]
            writer.writerow(cols)
            for r in self.parse_data():
                writer.writerow(r.values())

        logger.info(f'Number of rows is: {self.number_rows}')
        logger.info('Finished writing csv file')

        return 0

    def to_parquet(self,
                   output: Union[str, Path, PathLike, BinaryIO],
                   batch_size: int = 500,
                   parquet_version: str = '1.0') -> int:
        """Parse and convert to parquet

        Parameters
        ----------
        output : Union[str, Path, PathLike, BinaryIO]
            Output file. It is better to use file-like object.
        batch_size : int
            Number of rows to extract before writing to the parquet file.
            If None, the number of rows will be equal to 500. It is used for
            memory optimization.
        parquet_version : str
            Parquet version. Default is `1.0`. Please look at pyarrow
            documentation.

        Returns
        -------
        int:
            0 if the parsing and conversion are ok.
        """
        if isinstance(output, (str, Path, PathLike)):
            output = open(output, mode='wb')

        try:
            if not hasattr(output, 'mode'):
                raise TypeError('File-like object should have `mode` attribute')

            # Accept only write and text mode when opening output file
            if output.mode != 'wb':
                msg = 'File-like object should be opened in write and binary ' \
                      'mode'
                raise ValueError(msg)
        except Exception as e:
            logger.error(e)

        if batch_size is None:
            batch_size = 500

        if parquet_version is None:
            batch_size = '1.0'

        logger.info("Start parsing")
        logger.debug("Put the pointer at the beginning of the ixf file")
        self.file.seek(0)
        logger.debug("Parse header record")
        self.parse_header()
        logger.debug("Parse table record")
        self.parse_table()
        logger.debug("Parse column descriptor records")
        self.parse_columns()

        logger.debug("Start writing in the parquet file")
        parquet_schema = pyarrow.schema(
            get_pyarrow_schema(self.columns_info).items()
        )
        with output as of:
            with ParquetWriter(
                    of, parquet_schema, flavor='spark', version='1.0'
            ) as writer:
                for batch in get_batch(self.parse_data, size=batch_size):
                    data = [pyarrow.array(v) for v in batch.values()]
                    batch = pyarrow.record_batch(
                        data=data,
                        schema=parquet_schema
                    )
                    writer.write_batch(batch)

        logger.info(f'Number of rows is: {self.number_rows}')
        logger.info('Finished writing parquet file')

        return 0


__all__ = ['IXFParser']
