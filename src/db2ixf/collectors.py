# coding=utf-8
"""Collects data from fields extracted from data records."""
from datetime import datetime, date, time
from struct import unpack
from typing import Union


def collect_smallint(c, fields, pos, encoding) -> int:
    """Collects SMALLINT data type from ixf as an integer.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    int:
        Integer.
    """
    field = int(unpack('<i', fields[pos:pos + 2])[0])
    return field


def collect_integer(c, fields, pos, encoding) -> int:
    """Collects INTEGER data type from ixf as an integer.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    int:
        Integer.
    """
    field = int(unpack('<i', fields[pos:pos + 4])[0])
    return field


def collect_bigint(c, fields, pos, encoding) -> int:
    """Collects BIGINT data type from ixf as an integer.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    int:
        Integer.
    """
    field = int(unpack('<q', fields[pos:pos + 8])[0])
    return field


def collect_char(c, fields, pos, encoding) -> str:
    """Collects CHAR data type from ixf as a string.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    str:
        String.
    """
    length = int(c['IXFCLENG'])
    field = str(fields[pos:pos + length], encoding=encoding)
    return field.strip()


def collect_varchar(c, fields, pos, encoding) -> str:
    """Collects VARCHAR data type from ixf as a string.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    str:
        String.
    """
    length = int(unpack('<h', fields[pos:pos + 2])[0])
    pos += 2
    field = str(fields[pos:pos + length], encoding=encoding)
    return field.strip()


def collect_date(c, fields, pos, encoding) -> date:
    """Collects DATE data type from ixf as a date object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    date:
        Date of format yyyy-mm-dd.
    """
    field = str(fields[pos:pos + 10], encoding=encoding)
    return datetime.strptime(field, '%Y-%m-%d').date()


def collect_time(c, fields, pos, encoding) -> time:
    """Collects TIME data type from ixf as a time object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    time:
        Time of format HH:MM:SS.
    """
    field = str(fields[pos:pos + 8], encoding=encoding)
    return datetime.strptime(field, '%H.%M.%S').time()


def collect_timestamp(c, fields, pos, encoding) -> datetime:
    """Collects TIMESTAMP data type from ixf as a datetime object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    timestamp:
        Timestamp of format yyyy-mm-dd-HH.MM.SS.UUUUUU
    """
    field = str(fields[pos:pos + 26], encoding=encoding)
    return datetime.strptime(field, '%Y-%m-%d-%H.%M.%S.%f')


def collect_decimal(c, fields, pos, encoding) -> Union[int, float]:
    """Collects DECIMAL data type from ixf as a integer or a float.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF.
    fields : str
        Binary string containing data of the row.
    pos : int
        Position of the column in the `fields`.
    encoding : str
        Encoding of the ixf file.

    Returns
    -------
    Union[int, float]:
        Integer or Float
    """
    p = int(c['IXFCLENG'][0:3])
    s = int(c['IXFCLENG'][3:5])
    length = int((p + 2) / 2)
    field = fields[pos:pos + length]

    dec = 0.0
    for b in range(0, min(len(field), length) - 1):
        dec = dec * 100 + int(field[b] >> 4) * 10 + int(field[b] & 0x0f)
    dec = dec * 10 + int(field[-1] >> 4)

    if int(field[-1] & 0x0f) != 12:
        dec = -dec

    if s == 0:
        return int(dec)

    return dec / pow(10, s)
