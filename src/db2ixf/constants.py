# coding=utf-8
"""Contains constants about mappers, schemas, metadata and others"""
import os
from collections import OrderedDict
from datetime import date, datetime, time

# Records
HEADER_RECORD_TYPE = OrderedDict(
    {
        'IXFHRECL': 6,
        'IXFHRECT': 1,
        'IXFHID': 3,
        'IXFHVERS': 4,
        'IXFHPROD': 12,
        'IXFHDATE': 8,
        'IXFHTIME': 6,
        'IXFHHCNT': 5,
        'IXFHSBCP': 5,
        'IXFHDBCP': 5,
        'IXFHFIL1': 2
    }
)
"""Length in bytes of the fields in the header record."""

TABLE_RECORD_TYPE = OrderedDict(
    {
        'IXFTRECL': 6,
        'IXFTRECT': 1,
        'IXFTNAML': 3,
        'IXFTNAME': 256,
        'IXFTQULL': 3,
        'IXFTQUAL': 256,
        'IXFTSRC': 12,
        'IXFTDATA': 1,
        'IXFTFORM': 1,
        'IXFTMFRM': 5,
        'IXFTLOC': 1,
        'IXFTCCNT': 5,
        'IXFTFIL1': 2,
        'IXFTDESC': 30,
        'IXFTPKNM': 257,
        'IXFTDSPC': 257,
        'IXFTISPC': 257,
        'IXFTLSPC': 257
    }
)
"""Length in bytes of the fields in the table record."""

COL_DESCRIPTOR_RECORD_TYPE = OrderedDict(
    {
        'IXFCRECL': 6,
        'IXFCRECT': 1,
        'IXFCNAML': 3,
        'IXFCNAME': 256,
        'IXFCNULL': 1,
        'IXFCDEF': 1,
        'IXFCSLCT': 1,
        'IXFCKPOS': 2,
        'IXFCCLAS': 1,
        'IXFCTYPE': 3,
        'IXFCSBCP': 5,
        'IXFCDBCP': 5,
        'IXFCLENG': 5,
        'IXFCDRID': 3,
        'IXFCPOSN': 6,
        'IXFCDESC': 30,
        'IXFCLOBL': 20,
        'IXFCUDTL': 3,
        'IXFCUDTN': 256,
        'IXFCDEFL': 3,
        'IXFCDEFV': 254,
        'IXFCREF': 1,
        'IXFCNDIM': 2
        # 'IXFCDSIZ' : variable   ## this att is determined at runtime
    }
)
"""Length in bytes of the fields in the column descriptor record."""

DATA_RECORD_TYPE = OrderedDict(
    {
        'IXFDRECL': 6,
        'IXFDRECT': 1,
        'IXFDRID': 3,
        'IXFDFIL1': 4
        # 'IXFDCOLS': variable  ## this att is determined at runtime
    }
)
"""Length in bytes of the fields in the data record."""

APPLICATION_RECORD_TYPE = OrderedDict(
    {
        'IXFARECL': 6,
        'IXFARECT': 1,
        'IXFAPPID': 12,
        # 'IXFADATA': variable
    }
)
"""Length in bytes of the fields in the application record."""

# Data types
IXF_DTYPES = {
    384: 'DATE',
    388: 'TIME',
    392: 'TIMESTAMP',
    404: 'BLOB',
    408: 'CLOB',
    412: 'DBCLOB',
    448: 'VARCHAR',
    452: 'CHAR',
    456: 'LONGVARCHAR',
    464: 'VARGRAPHIC',
    468: 'GRAPHIC',
    472: 'LONG VARGRAPHIC',
    480: 'FLOATING POINT',
    484: 'DECIMAL',
    492: 'BIGINT',
    496: 'INTEGER',
    500: 'SMALLINT',
    908: 'VARBINARY',
    912: 'BINARY',
    916: 'BLOB_FILE',
    920: 'CLOB_FILE',
    924: 'DBCLOB_FILE',
    996: 'DECFLOAT'
}
"""IXF data types"""

# Mappers
IXF_TO_PYTHON_DTYPES = {
    'DATE': date,
    'TIME': time,
    'TIMESTAMP': datetime,
    'VARCHAR': str,
    'CHAR': str,
    'DECIMAL': float,
    'BIGINT': int,
    'INTEGER': int,
    'SMALLINT': int,
}
"""Maps IXF data types to python ones"""

# Data
DB2IXF_ACCEPTED_CORRUPTION_RATE = int(
    os.getenv("DB2IXF_ACCEPTED_CORRUPTION_RATE", "1")
)
"""Accepted rate of corrupted data, attention to data loss !"""

if not (0 <= DB2IXF_ACCEPTED_CORRUPTION_RATE <= 100):
    raise ValueError(
        "`DB2IXF_DATA_CORRUPTION_RATE` should be integer between 0 and 100"
    )

# Will need to delete this coz not necessary so skip it
CCSID_TO_CODE_PAGE = {
    37: 'cp037',
    273: 'cp273',
    277: 'cp277',
    278: 'cp278',
    280: 'cp280',
    284: 'cp284',
    285: 'cp285',
    297: 'cp297',
    300: 'cp300',
    301: 'cp301',
    420: 'cp420',
    424: 'cp424',
    437: 'cp437',
    500: 'cp500',
    737: 'cp737',
    775: 'cp775',
    808: 'cp808',
    813: 'cp813',
    819: 'cp819',
    833: 'cp833',
    834: 'cp834',
    835: 'cp835',
    836: 'cp836',
    837: 'cp837',
    850: 'cp850',
    852: 'cp852',
    855: 'cp855',
    856: 'cp856',
    857: 'cp857',
    858: 'cp858',
    859: 'cp859',
    860: 'cp860',
    861: 'cp861',
    862: 'cp862',
    863: 'cp863',
    864: 'cp864',
    865: 'cp865',
    866: 'cp866',
    867: 'cp867',
    868: 'cp868',
    869: 'cp869',
    870: 'cp870',
    871: 'cp871',
    874: 'cp874',
    875: 'cp875',
    897: 'cp897',
    912: 'cp912',
    915: 'cp915',
    916: 'cp916',
    918: 'cp918',
    920: 'cp920',
    921: 'cp921',
    922: 'cp922',
    923: 'cp923',
    924: 'cp924',
    927: 'cp927',
    930: 'cp930',
    932: 'cp932',
    933: 'cp933',
    935: 'cp935',
    937: 'cp937',
    939: 'cp939',
    942: 'cp942',
    943: 'cp943',
    947: 'cp947',
    948: 'cp948',
    949: 'cp949',
    950: 'cp950',
    951: 'cp951',
    954: 'cp954',
    964: 'cp964',
    970: 'cp970',
    971: 'cp971',
    1006: 'cp1006',
    1025: 'cp1025',
    1026: 'cp1026',
    1027: 'cp1027',
    1041: 'cp1041',
    1043: 'cp1043',
    1046: 'cp1046',
    1047: 'cp1047',
    1051: 'cp1051',
    1088: 'cp1088',
    1089: 'cp1089',
    1097: 'cp1097',
    1098: 'cp1098',
    1112: 'cp1112',
    1114: 'cp1114',
    1115: 'cp1115',
    1122: 'cp1122',
    1123: 'cp1123',
    1124: 'cp1124',
    1140: 'cp1140',
    1141: 'cp1141',
    1142: 'cp1142',
    1143: 'cp1143',
    1144: 'cp1144',
    1145: 'cp1145',
    1146: 'cp1146',
    1147: 'cp1147',
    1148: 'cp1148',
    1149: 'cp1149',
    1200: 'cp1200',
    1202: 'cp1202',
    1204: 'cp1204',
    1208: 'cp1208',
    1232: 'cp1232',
    1234: 'cp1234',
    1236: 'cp1236',
    1351: 'cp1351',
    1362: 'cp1362',
    1363: 'cp1363',
    1364: 'cp1364',
    1370: 'cp1370',
    1371: 'cp1371',
    1375: 'cp1375',
    1380: 'cp1380',
    1381: 'cp1381',
    1382: 'cp1382',
    1383: 'cp1383',
    1385: 'cp1385',
    1386: 'cp1386',
    1388: 'cp1388',
    1390: 'cp1390',
    1399: 'cp1399',
    5050: 'cp5050',
    5054: 'cp5054',
    5346: 'cp5346',
    5347: 'cp5347',
    5348: 'cp5348',
    5349: 'cp5349',
    5350: 'cp5350',
    5351: 'cp5351',
    5352: 'cp5352',
    5353: 'cp5353',
    5354: 'cp5354',
    5488: 'cp5488',
    9030: 'cp9030',
    9066: 'cp9066',
    9400: 'cp9400',
    25546: 'cp25546',
    33722: 'cp33722',
}
