# coding=utf-8
"""
Helps the user to parse PC/IXF file format of IBM DB2.

IXF file is organised in a sequence of records.
these records have 5 main types: Header, Table, Column Descriptor,
Data and Application.

Inside the IXF file, these records are ordered which means that it
starts with a header record, table one, set of column descriptors
- where each column descriptor is also a record - ant it ends with the set of
data records.

IXF = H + T + Set(C) + Set(D).

Each record type is represented by a list of fields and each field has a length
in bytes that we will use to read data from the IXF file.

For more information about record types; Please visit this
[link](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-record-types).


Data records [Set(D)] stores the data we want to extract, which means that
for each column we need to extract its content from the data record.
Each column has its data type.

For more information about data types; Please visit this
[link](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
"""
import codecs
from db2ixf.ibmcodecs import search_functions
from db2ixf.ixf import IXFParser

for sf in search_functions:
    codecs.register(sf)

__all__ = ["IXFParser"]
