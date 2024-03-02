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
    os.getenv("DB2IXF_ACCEPTED_CORRUPTION_RATE", 1)
)
"""Accepted rate of corrupted data, attention to data loss !"""

if not (0 <= DB2IXF_ACCEPTED_CORRUPTION_RATE <= 100):
    raise ValueError(
        "`DB2IXF_DATA_CORRUPTION_RATE` should be integer between 0 and 100"
    )

MAX_SIZE_IXF_DATA_RECORD = 32 * 1024
"""See IBM Doc: Max size of the data area of a data record in ixf format is 
around 32 KB.
"""

DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER = int(
    os.getenv(
        "BUFFER_SIZE_CLI_CLOUD_PROVIDER", 4 * 1024 * 1024  # 4MB (Azure client)
    )
)
"""Buffer size of clients of cloud providers storage services"""

if DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER == 0:
    raise ValueError(
        "`DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER`=# of Bytes should be > 0"
    )

DB2IXF_DEFAULT_BATCH_SIZE = os.getenv(
    "DB2IXF_DEFAULT_BATCH_SIZE",
    int(DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER / MAX_SIZE_IXF_DATA_RECORD)
)
"""Batch size (number of rows), defaults to 128"""
