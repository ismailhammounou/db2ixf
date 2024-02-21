# coding=utf-8
"""Collects data from the fields extracted from the data records (D)."""
from datetime import date, datetime, time
from db2ixf.exceptions import DataCollectorError
from db2ixf.helpers import decode_cell, get_ccsid_from_column
from decimal import Decimal
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
    str
        Binary string.

    Raises
    ------
    DataCollectorError
        When length exceeds 254 bytes.
    """
    length = int(c["IXFCLENG"])

    if length > 254:
        msg = "Length of a binary data types should not exceed 254 bytes."
        raise DataCollectorError(msg)

    field = fields[pos:pos + length]

    return field


def collect_smallint(c, fields, pos) -> int:  # noqa
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
    int
        Integer.
    """
    field = int(unpack("<h", fields[pos:pos + 2])[0])

    return field


def collect_integer(c, fields, pos) -> int:  # noqa
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
    int
        Integer.
    """
    field = int(unpack("<i", fields[pos:pos + 4])[0])

    return field


def collect_bigint(c, fields, pos) -> int:  # noqa
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
    int
        Integer.
    """
    field = int(unpack("<q", fields[pos:pos + 8])[0])

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
    Union[int, float]
        Integer or Float.
    """
    p = int(c["IXFCLENG"][0:3])
    s = int(c["IXFCLENG"][3:5])
    length = int((p + 2) / 2)
    field = fields[pos:pos + length]

    dec = 0.0
    for b in range(0, min(len(field), length) - 1):
        dec = dec * 100 + int(field[b] >> 4) * 10 + int(field[b] & 0x0f)
    dec = dec * 10 + int(field[-1] >> 4)

    if int(field[-1] & 0x0f) != 12:
        dec = -dec

    if s == 0:
        return Decimal(dec)

    return Decimal(dec / pow(10, s))


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

    Raises
    ------
    DataCollectorError
        When facing extra bytes.
    """
    col_length = int(c["IXFCLENG"])

    if col_length == 4:
        field = float(unpack(">f", fields[pos:pos + col_length])[0])
        return field

    if col_length == 8:
        field = float(unpack(">d", fields[pos:pos + col_length])[0])
        return field

    raise DataCollectorError(
        f"Expecting 4 or 8 bytes, found {col_length} bytes"
    )


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

    Raises
    ------
    DataCollectorError
        When length exceeds 254 bytes.
    """
    length = int(c["IXFCLENG"])

    if length > 254:
        msg = "Length of a char data types should not exceed 254 bytes."
        raise DataCollectorError(msg)

    sbcp, dbcp = get_ccsid_from_column(c)

    field = fields[pos:pos + length]

    if dbcp != 0:
        return decode_cell(field, dbcp, "d").strip()

    if sbcp != 0:
        return decode_cell(field, sbcp).strip()

    return str(field, "utf-8").strip()


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
    str
        String.

    Raises
    ------
    DataCollectorError
        When length of var char exceeds maximum length.
    """
    max_length = int(c["IXFCLENG"])

    length = int(unpack("<h", fields[pos:pos + 2])[0])
    if length > max_length:
        msg = f"Length {length} exceeds the maximum length {max_length}."
        raise DataCollectorError(msg)

    pos += 2

    sbcp, dbcp = get_ccsid_from_column(c)

    field = fields[pos:pos + length]

    if dbcp != 0:
        return decode_cell(field, dbcp, "d").strip()

    if sbcp != 0:
        return decode_cell(field, sbcp).strip()

    return str(field, "utf-8").strip()


def collect_longvarchar(c, fields, pos) -> str:
    """Collects LONGVARCHAR data type from ixf as a string.

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

    Raises
    ------
    DataCollectorError
        When length of long var char exceeds maximum length.
    """
    max_length = int(c["IXFCLENG"])
    length = int(unpack("<h", fields[pos:pos + 2])[0])
    if length > max_length:
        msg = f"Length {length} exceeds the maximum length {max_length}."
        raise DataCollectorError(msg)

    pos += 2

    sbcp, dbcp = get_ccsid_from_column(c)

    field = fields[pos:pos + length]

    if dbcp != 0:
        return decode_cell(field, dbcp, "d").strip()

    if sbcp != 0:
        return decode_cell(field, sbcp).strip()

    return str(field, "utf-8").strip()


def collect_vargraphic(c, fields, pos) -> str:
    """Collects VARGRAPHIC data type from ixf as a string.

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

    Raises
    ------
    DataCollectorError
        When length of var graphic exceeds maximum length.
    """
    max_length = int(c["IXFCLENG"])

    length = int(unpack("<h", fields[pos:pos + 2])[0])
    if length > max_length:
        msg = f"Length {length} exceeds the maximum length {max_length}."
        raise DataCollectorError(msg)

    pos += 2

    _, dbcp = get_ccsid_from_column(c)

    field = fields[pos:pos + (length * 2)]

    if dbcp != 0:
        return decode_cell(field, dbcp, "d").strip()

    _msg = "The string in double-byte characters has DBCS code page " \
           "equals to 0 (unknown encoding)"
    raise DataCollectorError(_msg)


def collect_date(c, fields, pos) -> date:  # noqa
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
    date
        Date of format yyyy-mm-dd.
    """
    field = str(fields[pos:pos + 10], encoding="utf-8").strip()

    return datetime.strptime(field, "%Y-%m-%d").date()


def collect_time(c, fields, pos) -> time:  # noqa
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
    time
        Time of format HH:MM:SS.
    """
    field = str(fields[pos:pos + 8], encoding="utf-8").strip()

    return datetime.strptime(field, "%H.%M.%S").time()


def collect_timestamp(c, fields, pos) -> datetime:  # noqa
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
    datetime
        Timestamp of format yyyy-mm-dd-hh.mm.ss.nnnnnn or yyyy-mm-dd-hh.mm.ss.
    """
    field = str(fields[pos:pos + 26], encoding="utf-8").strip()

    try:
        return datetime.strptime(field, "%Y-%m-%d-%H.%M.%S.%f")
    except ValueError:
        return datetime.strptime(field, "%Y-%m-%d-%H.%M.%S")


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
    DataCollectorError
        When length of the large object exceeds the maximum length Or
        When SBCP and DBCP are simultaneously equal to 0.
    """
    max_length = int(c["IXFCLENG"])

    length = int(unpack("<i", fields[pos:pos + 4])[0])
    if length > max_length:
        msg = f"Length {length} exceeds the maximum length {max_length}."
        raise DataCollectorError(msg)

    pos += 4

    sbcp, dbcp = get_ccsid_from_column(c)

    field = fields[pos:pos + length]

    if dbcp != 0:
        return decode_cell(field, dbcp, "d").strip()

    if sbcp != 0:
        return decode_cell(field, sbcp).strip()

    msg = "CLOB data type can not be a bit string as BLOB, " \
          "the SBCP and DBCP should not simultaneously be equal to 0."
    raise DataCollectorError(msg)


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
    DataCollectorError
        When the length of the binary large object exceeds the maximum length.
    """
    max_length = int(c["IXFCLENG"])

    length = int(unpack("<i", fields[pos:pos + 4])[0])
    if length > max_length:
        msg = f"Length {length} exceeds the maximum length {max_length}."
        raise DataCollectorError(msg)

    pos += 4

    sbcp, dbcp = get_ccsid_from_column(c)

    field = fields[pos:pos + length]

    if dbcp != 0:
        return decode_cell(field, dbcp, "d").strip()

    if sbcp != 0:
        return decode_cell(field, sbcp).strip()

    return field


# Map between ixf data type code and its collector
collectors = {
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

__all__ = ["collectors"]
