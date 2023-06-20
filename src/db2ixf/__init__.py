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
import ebcdic
from db2ixf.ibmcodecs import (ibm_utf_32_be,
                              ibm_utf_32_le,
                              ibm_utf_32,
                              ibm_utf_16_be,
                              ibm_utf_16_le,
                              ibm_utf_16,
                              ibm_utf_8,
                              ibm_latin1,
                              ibm_latin9,
                              ibm_37,
                              ibm_39,
                              ibm_813,
                              ibm_859,
                              ibm_867,
                              ibm_874,
                              ibm_912,
                              ibm_915,
                              ibm_916,
                              ibm_920,
                              ibm_921,
                              ibm_922,
                              ibm_923,
                              ibm_924,
                              ibm_943,
                              ibm_947,
                              ibm_951,
                              ibm_954,
                              ibm_964,
                              ibm_970,
                              ibm_1088,
                              ibm_1089,
                              ibm_1098,
                              ibm_1114,
                              ibm_1115,
                              ibm_1124,
                              ibm_1351,
                              ibm_1362,
                              ibm_1363,
                              ibm_1375,
                              ibm_1380,
                              ibm_1381,
                              ibm_1383,
                              ibm_1385,
                              ibm_1386,
                              ibm_1390,
                              ibm_1392,
                              ibm_5050,
                              ibm_5054,
                              ibm_5346,
                              ibm_5347,
                              ibm_5348,
                              ibm_5349,
                              ibm_5350,
                              ibm_5351,
                              ibm_5352,
                              ibm_5353,
                              ibm_5354,
                              ibm_5488,
                              ibm_9030,
                              ibm_9066,
                              ibm_25546,
                              ibm_33722)
from db2ixf.ixf import IXFParser

search_functions = (
    ebcdic._find_ebcdic_codec,
    ibm_utf_32_be,
    ibm_utf_32_le,
    ibm_utf_32,
    ibm_utf_16_be,
    ibm_utf_16_le,
    ibm_utf_16,
    ibm_utf_8,
    ibm_latin1,
    ibm_latin9,
    ibm_37,
    ibm_39,
    ibm_813,
    ibm_859,
    ibm_867,
    ibm_874,
    ibm_912,
    ibm_915,
    ibm_916,
    ibm_920,
    ibm_921,
    ibm_922,
    ibm_923,
    ibm_924,
    ibm_943,
    ibm_947,
    ibm_951,
    ibm_954,
    ibm_964,
    ibm_970,
    ibm_1088,
    ibm_1089,
    ibm_1098,
    ibm_1114,
    ibm_1115,
    ibm_1124,
    ibm_1351,
    ibm_1362,
    ibm_1363,
    ibm_1375,
    ibm_1380,
    ibm_1381,
    ibm_1383,
    ibm_1385,
    ibm_1386,
    ibm_1390,
    ibm_1392,
    ibm_5050,
    ibm_5054,
    ibm_5346,
    ibm_5347,
    ibm_5348,
    ibm_5349,
    ibm_5350,
    ibm_5351,
    ibm_5352,
    ibm_5353,
    ibm_5354,
    ibm_5488,
    ibm_9030,
    ibm_9066,
    ibm_25546,
    ibm_33722,
)

for sf in search_functions:
    codecs.register(sf)

__all__ = ['IXFParser']
