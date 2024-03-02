# coding=utf-8
"""Create helper function for schema generation and others."""
import chardet
import os
import warnings
from collections import OrderedDict
from db2ixf.constants import (
    DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER, DB2IXF_DEFAULT_BATCH_SIZE, IXF_DTYPES,
)
from db2ixf.exceptions import NotValidDataPrecisionException
from db2ixf.logger import logger
from pyarrow import (
    RecordBatch, Schema, array, binary, date32, decimal128, decimal256, field,
    float32, float64, int16, int32, int64, large_binary, large_string,
    record_batch, schema, string, time32, time64, timestamp,
)
from typing import (BinaryIO, List, Literal, Tuple)


def get_filesize(file: BinaryIO) -> int:
    if hasattr(file, "seek"):
        filesize = file.seek(0, os.SEEK_END)
        file.seek(0)
        return filesize
    if hasattr(file, "fs"):
        filesize = file.fs.size(file.path)
        return filesize
    if hasattr(file, "open"):
        filesize = file.open(file.path).seek(0, os.SEEK_END)
        file.open(file.path).seek(0)
        return filesize
    return 0


def init_opt_batch_size(file_size: int):
    """Init optimal batch size"""
    nbr_net_req = int(file_size / DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER)
    if nbr_net_req == 0:
        nbr_net_req = 1
    return int(nbr_net_req * DB2IXF_DEFAULT_BATCH_SIZE * 1.5)


def get_opt_batch_size(batch_size: int, row_size: int) -> int:
    size = int(DB2IXF_BUFFER_SIZE_CLOUD_PROVIDER / row_size * 1.5)
    return max(batch_size, size)


def get_pyarrow_schema(cols: List[OrderedDict]) -> Schema:
    """
    Creates a pyarrow schema of the columns extracted from IXF file.

    Parameters
    ----------
    cols : List[OrderedDict]
        List of column descriptors extracted from IXF file.

    Returns
    -------
    Schema
        Pyarrow Schema extracted from columns description.
    """

    mapper = {
        "DATE": date32(),
        "TIME": time64("ns"),
        "TIMESTAMP": timestamp("ns"),
        "BLOB": large_binary(),
        "CLOB": large_string(),
        "VARCHAR": string(),
        "CHAR": string(),
        "LONGVARCHAR": string(),
        "VARGRAPHIC": string(),
        "FLOATING POINT": float64(),
        "DECIMAL": decimal128(19),
        "BIGINT": int64(),
        "INTEGER": int32(),
        "SMALLINT": int16(),
        "BINARY": binary(),
    }

    # todo: use the code page from the header instead of utf-8
    _schema = []
    for c in cols:
        cname = c["IXFCNAME"].decode("utf-8").strip()
        cdesc = c["IXFCDESC"].decode("utf-8").strip()
        cnull = c["IXFCNULL"].decode("utf-8").strip()
        ctype = int(c["IXFCTYPE"])

        # Update dtype for datatypes
        dtype = mapper[IXF_DTYPES[ctype]]
        if ctype == 912:
            length = int(c["IXFCLENG"])
            dtype = binary(length)

        if ctype == 480:
            length = int(c["IXFCLENG"])
            dtype = float32() if length == 4 else dtype

        if ctype == 484:
            precision = int(c["IXFCLENG"][0:3])
            scale = int(c["IXFCLENG"][3:5])
            if precision <= 38:
                if scale == 0:
                    dtype = int64()
                else:
                    dtype = decimal128(precision, scale)
            else:
                dtype = decimal256(precision, scale)

        if ctype == 392:
            fsp = int(c["IXFCLENG"])
            if fsp == 0:
                dtype = timestamp("s")
            elif 0 < fsp <= 3:
                dtype = timestamp("ms")
            elif 3 < fsp <= 6:
                dtype = timestamp("us")
            elif 6 < fsp <= 12:
                dtype = timestamp("ns")
            else:
                msg = f"Invalid time precision for {cname}, expected < 12"
                raise NotValidDataPrecisionException(msg)

        # See if the col is nullable or not
        if cnull.lower() not in ["y", "n"]:
            cnull = "Y"
        cnullable = False if cnull.lower() == "n" else True

        _field = field(
            cname,
            dtype,
            nullable=cnullable,
            metadata={cname: cdesc}
        )

        _schema.append(_field)

    return schema(_schema)


def get_column_names(cols: List[OrderedDict]) -> List[str]:
    names = []
    for col in cols:
        name = str(col["IXFCNAME"], encoding="utf-8").strip()
        names.append(name)
    return names


def get_ccsid_from_column(column: OrderedDict) -> Tuple[int, int]:
    """
    Get the coded character set identifiers for single and double bytes
    data type. Which means the code page for singular/double byte data type.
    """
    sbcp = str(column["IXFCSBCP"], "utf-8").strip()
    dbcp = str(column["IXFCDBCP"], "utf-8").strip()

    sbcp = int(sbcp) if sbcp else 0
    dbcp = int(dbcp) if dbcp else 0

    return sbcp, dbcp


def deltalake_fix_ns_timestamps(pyarrow_schema: Schema) -> Schema:
    """Fix issue with timestamps in deltalake.

    Deltalake has issue with timestamps in nanoseconds and it does not yet
    support it, so this function changes the pyarrow timestamp datatype
    in nanoseconds to microseconds. pyarrow timestamp datatype in microseconds
    is supported.

    Parameters
    ----------
    pyarrow_schema : Schema
        Pyarrow schema

    Returns
    -------
    Schema:
        Pyarrow schema with fix
    """
    for i, f in enumerate(pyarrow_schema):
        if f.type == timestamp("ns"):
            new_field = field(
                f.name,
                timestamp("us"),
                nullable=f.nullable,
                metadata=f.metadata
            )
            pyarrow_schema = pyarrow_schema.set(i, new_field)
    return pyarrow_schema


def deltalake_fix_time(pyarrow_schema: Schema) -> Schema:
    """Fix issue with time in deltalake.

    Deltalake does not support time datatype so we will try to use string to
    temporary fix the issue. Pyarrow schema has time64 and time32 datatypes but
    it is complicated for now to cast them to timestamp because the later is
    supported by deltalake. For this later reason, this function will use
    pyarrow string datatype to replace pyarrow time datatypes until casting
    pyarrow time datatype as a datetime is possible in deltalake or support of
    pyarrow time datatype in deltalake is added.

    Parameters
    ----------
    pyarrow_schema : Schema
        Pyarrow schema

    Returns
    -------
    Schema
        Pyarrow schema with the fix.
    """
    time_datatypes = {
        time64("ns"),
        time64("us"),
        time32("ms"),
        time32("s"),
    }
    for i, f in enumerate(pyarrow_schema):
        if f.type in time_datatypes:
            new_field = field(
                f.name,
                string(),
                nullable=f.nullable,
                metadata=f.metadata
            )
            pyarrow_schema = pyarrow_schema.set(i, new_field)
    return pyarrow_schema


def apply_schema_fixes(pyarrow_schema: Schema) -> Schema:
    """Apply all fixes on pyarrow schema to adapt to deltalake.

    Fixes issues in deltalake support for nanoseconds unit for time and
    timestamp datatype.

    Parameters
    ----------
    pyarrow_schema : Schema
        Pyarrow schema

    Returns
    -------
    Schema:
        Pyarrow schema with all fixes
    """
    fixes = [deltalake_fix_ns_timestamps, deltalake_fix_time]
    for fix in fixes:
        pyarrow_schema = fix(pyarrow_schema)
    return pyarrow_schema


def to_pyarrow_record_batch(
    batch: dict,
    pyarrow_schema: Schema
) -> RecordBatch:
    """Transforms to pyarrow record batch.

    Parameters
    ----------
    batch : DefaultOrderedDict
        Dictionary of type Dict[str, list]
    pyarrow_schema: Schema
        Pyarrow schema

    Returns
    -------
    RecordBatch
        Pyarrow record batch
    """
    _arrays = []
    for k, v in batch.items():
        _dtype = pyarrow_schema.field(k).type
        _arrays.append(array(v, type=_dtype))
        _dtype = None

    return record_batch(_arrays, schema=pyarrow_schema)


def decode_cell(cell: str, cp: int, cpt: Literal["s", "d"] = "s"):
    """Try to decode the cell using the provided codepage.

    Parameters
    ----------
    cell : str
        Field containing data
    cp : int
        IBM code page
    cpt : Literal["s", "d"]
        Defaults to `s` which means single byte and `d` means double bytes

    Returns
    -------
    str:
        Decoded cell
    """
    if cpt not in ["s", "d"]:
        raise ValueError("Either `s` for single bytes or `d` for double bytes")

    try:
        return cell.decode(f"cp{cp}")
    except UnicodeDecodeError:
        logger.debug("Trying cp437 encoding")
        try:
            return cell.decode("cp437")
        except UnicodeDecodeError:
            try:
                logger.debug("Trying to detect the encoding")
                _encoding = chardet.detect(cell, True)["encoding"]
                return cell.decode(_encoding)
            except UnicodeDecodeError as err:
                logger.debug(f"Detected encoding fails: {err}")
                try:
                    if cpt == "s":
                        logger.debug("Trying utf-8 encoding")
                        return cell.decode("utf-8")
                    else:
                        try:
                            logger.debug("Trying utf-16 encoding")
                            return cell.decode("utf-16")
                        except UnicodeDecodeError:
                            logger.debug("Trying utf-32 encoding")
                            return cell.decode("utf-32")
                except UnicodeDecodeError:
                    logger.debug(
                        "Alert: eventual data loss, please provide encoding !"
                    )
                    return cell.decode(f"cp{cp}", errors="ignore")


def deprecated(version: str, message: str = ""):
    def decorator(func):
        _info = f"WARNING: `{func.__name__}` is deprecated and will be " \
                f"removed in version {version}. "
        _info = f"{_info}{message}"

        def wrapper(*args, **kwargs):
            warnings.warn(_info, DeprecationWarning, stacklevel=2)
            return func(*args, **kwargs)

        return wrapper

    return decorator
