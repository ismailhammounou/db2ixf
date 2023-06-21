# coding=utf-8
"""Collects data from the fields extracted from the data records (D)."""
from datetime import datetime, date, time
from db2ixf.exceptions import (LargeObjectLengthException,
                               BinaryLengthException,
                               CLOBCodePageException,
                               CharLengthException,
                               VarCharLengthException)
from db2ixf.helpers import get_ccsid_from_column
from db2ixf.logger import logger
from struct import unpack
from typing import Union


def collect_binary(c, fields, pos) -> str:
    """Collects BINARY data type from ixf as a string.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    str:
        a binary string data.
    """
    length = int(c['IXFCLENG'])
    if length > 254:
        msg = 'Length of a binary data types should not exceed 254 bytes.'
        raise BinaryLengthException(msg)

    field = str(fields[pos:pos + length], 'utf-8')

    return field


def collect_smallint(c, fields, pos) -> int:
    """Collects SMALLINT data type from ixf as an integer.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    int:
        Integer.
    """
    field = int(unpack('<h', fields[pos:pos + 2])[0])
    return field


def collect_integer(c, fields, pos) -> int:
    """Collects INTEGER data type from ixf as an integer.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    int:
        Integer.
    """
    field = int(unpack('<i', fields[pos:pos + 4])[0])
    return field


def collect_bigint(c, fields, pos) -> int:
    """Collects BIGINT data type from ixf as an integer.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    int:
        Integer.
    """
    field = int(unpack('<q', fields[pos:pos + 8])[0])
    return field


def collect_decimal(c, fields, pos) -> Union[int, float]:
    """Collects DECIMAL data type from ixf as a integer or a float.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

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


def collect_floating_point(c, fields, pos) -> float:
    """Collects FLOATING POINT data type from ixf as a float.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    float
        A python float object.
    """
    length = int(c['IXFCLENG'])
    fmt = '!d' if length == 8 else '!f'
    field = float(unpack(fmt, fields[pos:pos + length])[0])
    return field


def collect_char(c, fields, pos) -> str:
    """Collects CHAR data type from ixf as a string.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    str
        String.
    """
    length = int(c['IXFCLENG'])
    if length > 254:
        msg = 'Length of a char data types should not exceed 254 bytes.'
        raise CharLengthException(msg)

    sbcp, dbcp = get_ccsid_from_column(c)

    if dbcp != 0:
        field = fields[pos:pos + length].decode(f'cp{dbcp}')
    else:
        if sbcp == 0:
            field = str(fields[pos:pos + length], 'utf-8')
        else:
            field = fields[pos:pos + length].decode(f'cp{sbcp}')

    return field.strip()


def collect_varchar(c, fields, pos) -> str:
    """Collects VARCHAR data type from ixf as a string.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    str:
        String.

    Raises
    ------
    VarCharLengthException
        Length of var char exceeds maximum length.
    """
    max_length = int(c['IXFCLENG'])
    # if max_length > 254:
    #     msg = f'Max length of a varchar data type (={max_length}) ' \
    #           f'must be less than 254 bytes.'
    #     raise ExceedingDefinedMaximumLengthException(msg)

    length = int(unpack('<h', fields[pos:pos + 2])[0])
    if length > max_length:
        msg = f'Length {length} exceeds the maximum length {max_length}.'
        raise VarCharLengthException(msg)

    pos += 2

    sbcp, dbcp = get_ccsid_from_column(c)

    if dbcp != 0:
        field = fields[pos:pos + length].decode(f'cp{dbcp}')
    else:
        if sbcp == 0:
            field = str(fields[pos:pos + length], 'utf-8')
        else:
            field = fields[pos:pos + length].decode(f'cp{sbcp}')

    return field.strip()


def collect_date(c, fields, pos) -> date:
    """Collects DATE data type from ixf as a date object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    date:
        Date of format yyyy-mm-dd.
    """
    field = str(fields[pos:pos + 10], encoding='utf-8')
    return datetime.strptime(field, '%Y-%m-%d').date()


def collect_time(c, fields, pos) -> time:
    """Collects TIME data type from ixf as a time object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    time:
        Time of format HH:MM:SS.
    """
    field = str(fields[pos:pos + 8], encoding='utf-8')
    return datetime.strptime(field, '%H.%M.%S').time()


def collect_timestamp(c, fields, pos) -> datetime:
    """Collects TIMESTAMP data type from ixf as a datetime object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    timestamp:
        Timestamp of format yyyy-mm-dd-HH.MM.SS.UUUUUU

    Raises
    ------
    LargeObjectLengthException
        When the length of the large object exceeds the maximum length.
    """
    field = str(fields[pos:pos + 26], encoding='utf-8')
    return datetime.strptime(field, '%Y-%m-%d-%H.%M.%S.%f')


def collect_clob(c, fields, pos) -> str:
    """Collects CLOB data type from ixf as a string object.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    str
        String representing the CLOB (Character Large Object).

    Raises
    ------
    LargeObjectLengthException
        When the length of the large object exceeds the maximum length.
    CLOBCodePageException
        When SBCP and DBCP are simultaneously equal to 0.
    """
    max_length = int(c['IXFCLENG'])
    # if max_length > 32767:
    #     msg = f'For CLOB data type, max length (={max_length}) must be ' \
    #           f'less than 32767 Bytes.'
    #     raise ExceedingDefinedMaximumLengthException(msg)

    length = int(unpack('<i', fields[pos:pos + 4])[0])
    if length > max_length:
        msg = f'Length {length} exceeds the maximum length {max_length}.'
        logger.error(msg)
        raise LargeObjectLengthException(msg)

    pos += 4

    sbcp, dbcp = get_ccsid_from_column(c)

    if dbcp != 0:
        field = fields[pos:pos + length].decode(f'cp{dbcp}')
    else:
        if sbcp == 0:
            msg = 'CLOB data type can not be a bit string as BLOB, ' \
                  'the SBCP and DBCP should not simultaneously be equal to 0.'
            logger.error(msg)
            raise CLOBCodePageException(msg)
        else:
            field = fields[pos:pos + length].decode(f'cp{sbcp}')

    return field.strip()


def collect_blob(c, fields, pos) -> str:
    """Collects BLOB data type from ixf as a string.

    Parameters
    ----------
    c : dict
        Column descriptor extracted from IXF file.
    fields : str
        Bytes string containing data of the row.
    pos : int
        Position of the column in the `fields`.

    Returns
    -------
    str
        string representing the BLOB (Blob Large Object).

    Raises
    ------
    LargeObjectLengthException
        When the length of the large object exceeds the maximum length.
    """
    max_length = int(c['IXFCLENG'])
    # if max_length > 32767:
    #     msg = 'For BLOB data type, max length must be less than 32767 Bytes.'
    #     raise ExceedingDefinedMaximumLengthException(msg)

    length = int(unpack('<i', fields[pos:pos + 4])[0])
    if length > max_length:
        msg = f'Length {length} exceeds the maximum length {max_length}.'
        logger.error(msg)
        raise LargeObjectLengthException(msg)

    pos += 4
    field = str(fields[pos:pos + length], 'utf-8')

    return field.strip()
