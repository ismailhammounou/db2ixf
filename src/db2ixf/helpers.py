# coding=utf-8
"""Create helper function for schema generation and others."""
import chardet
import pyarrow as pa
from db2ixf.constants import IXF_DTYPES
from db2ixf.exceptions import NotValidDataPrecisionException
from db2ixf.logger import logger
from typing import BinaryIO, Dict, Iterable, List, Literal, Tuple


def get_pyarrow_schema(cols: List[dict]) -> pa.Schema:
    """
    Creates a pyarrow schema of the columns extracted from IXF file.

    Parameters
    ----------
    cols : list[dict]
        List of column descriptors extracted from IXF file.

    Returns
    -------
    dict[str, object]
        Maps columns extracted from IXF file to their pyarrow data types.
    """

    mapper = {
        "DATE": pa.date32(),
        "TIME": pa.time64("ns"),
        "TIMESTAMP": pa.timestamp("ns"),
        "BLOB": pa.large_binary(),
        "CLOB": pa.large_string(),
        "VARCHAR": pa.string(),
        "CHAR": pa.string(),
        "LONGVARCHAR": pa.string(),
        "VARGRAPHIC": pa.string(),
        "FLOATING POINT": pa.float64(),
        "DECIMAL": pa.decimal128(19),
        "BIGINT": pa.int64(),
        "INTEGER": pa.int32(),
        "SMALLINT": pa.int16(),
        "BINARY": pa.binary(),
    }

    _schema = {}
    for c in cols:
        cname = c["IXFCNAME"].decode("utf-8").strip()
        ctype = int(c["IXFCTYPE"])
        dtype = mapper[IXF_DTYPES[ctype]]

        if ctype == 912:
            length = int(c["IXFCLENG"])
            dtype = pa.binary(length)

        if ctype == 480:
            length = int(c["IXFCLENG"])
            dtype = pa.float32() if length == 4 else dtype

        if ctype == 484:
            precision = int(c["IXFCLENG"][0:3])
            scale = int(c["IXFCLENG"][3:5])
            if scale == 0:
                dtype = pa.int64()
            else:
                dtype = pa.decimal256(precision, scale)

        if ctype == 392:
            fsp = int(c["IXFCLENG"])
            if fsp == 0:
                dtype = pa.timestamp("s")
            elif 0 < fsp <= 3:
                dtype = pa.timestamp("ms")
            elif 3 < fsp <= 6:
                dtype = pa.timestamp("us")
            elif 6 < fsp <= 12:
                dtype = pa.timestamp("ns")
            else:
                msg = f"Invalid time precision for {cname}, expected < 12"
                raise NotValidDataPrecisionException(msg)

        _schema[cname] = dtype

    return pa.schema(_schema.items())


def get_pandas_schema(cols: List[dict]) -> Dict[str, object]:
    """Creates a pandas schema of the columns extracted from IXF file.

    Parameters
    ----------
    cols : list[dict]
        List of column descriptors extracted from IXF file.

    Returns
    -------
    dict[str, object]:
        Maps columns extracted from IXF file to their pandas data types.
    """

    mapper = {
        "DATE": "datetime64[ns]",
        "TIME": "datetime64[ns]",
        "TIMESTAMP": "datetime64[ns]",
        "BLOB": bytes,
        "CLOB": object,
        "VARCHAR": object,
        "CHAR": object,
        "LONGVARCHAR": object,
        "VARGRAPHIC": object,
        "FLOATING POINT": "float64",
        "DECIMAL": "float32",
        "BIGINT": "int64",
        "INTEGER": "int64",
        "SMALLINT": "int64",
        "BINARY": bytes,
    }

    schema = {}
    for c in cols:
        cname = str(c["IXFCNAME"], encoding="utf-8").strip()
        ctype = int(c["IXFCTYPE"])
        dtype = mapper[IXF_DTYPES[ctype]]

        if ctype == 480:
            length = int(c["IXFCLENG"])
            dtype = "float32" if length == 4 else dtype

        if ctype == 484:
            scale = int(c["IXFCLENG"][3:5])
            if scale == 0:
                dtype = "int64"
            else:
                dtype = "float32"

        schema[cname] = dtype

    return schema


def get_batch(data: Iterable[Dict], size: int = 10000) -> Iterable[List[Dict]]:
    """Batch generator. It yields batch of rows/dictionaries as a list.

    Parameters
    ----------
    data : Iterable[Dict]
        Iterable of individual rows from the source data.
    size : int, optional
        Size of each batch (number of rows per batch).

    Returns
    -------
    Iterable[List[Dict]]
        Iterable of a list of rows.
    """
    batch = []
    for i, row in enumerate(data):
        batch.append(row)
        if (i + 1) % size == 0:
            yield batch
            batch = []

    # Yield the remaining rows as the last batch
    if batch:
        yield batch


def merge_dicts(dicts: List[dict]) -> Dict[str, list]:
    """
    Merge a list of dictionaries into a single dictionary where each key is
    mapped to a list of its values.

    Parameters
    ----------
    dicts : list
        A list of dictionaries.

    Returns
    -------
    dict[str, list]
        A dictionary where each key is mapped to a list of values.

    Examples
    --------
    >>> ex = [{"key1": "value1", "key2": "value2"}] # noqa
    >>> ex.append({"key1": "value3", "key2": "value4"})
    >>> merge_dicts(ex)
    {"key1": ["value1", "value3"], "key2": ["value2", "value4"]}
    """

    result = {}

    for dictionary in dicts:
        for key, value in dictionary.items():
            result.setdefault(key, []).append(value)

    return result


def get_array_batch(data_source: Iterable, size: int = 10000) -> Iterable[dict]:
    """Array batch generator. It yields a batch of rows in a single dictionary.

    It gets a list of size `size` containing rows from the data source
    then merge all rows in one dictionary and yield it.


    Parameters
    ----------
    data_source : Iterable
        Iterable of individual rows from the source data.
    size : int, optional
        Size of each batch (number of rows per batch). Default is 1000.

    Yields
    ------
    Iterable[Dict]
        A generator that yields batches of rows, where each batch is a
        list of rows.

    Examples
    --------
    Get a batch generator from a data generator and process the batches:

    >>> data_generator = some_data_generator  # Assuming yields rows  # noqa
    >>> batch_generator = get_array_batch(data_generator, size=100)

    >>> for b in batch_generator:
    ...     # Process the batch of rows
    ...     process_batch(b) # noqa

    Notes
    -----
    - The function accumulates rows until the number of rows reaches the
      specified `size`.
    - Once the accumulated rows reach the `size`, a batch is formed and yielded.
    - If there are remaining rows that do not form a complete batch, they are
      yielded as the last batch.
    - The `merge_dicts` function should be implemented separately and used
      to merge the rows into a single dictionary.
    """
    rows = []
    for i, row in enumerate(data_source):
        rows.append(row)
        if (i + 1) % size == 0:
            batch = merge_dicts(rows)
            yield batch
            rows = []

    # Yield the remaining rows as the last batch
    if rows:
        batch = merge_dicts(rows)
        yield batch


def get_ccsid_from_column(column: dict) -> Tuple[int, int]:
    """
    Get the coded character set identifiers for single and double bytes
    data type. Which means the code page for singular/double byte data type.
    """
    sbcp = str(column["IXFCSBCP"], "utf-8").strip()
    dbcp = str(column["IXFCDBCP"], "utf-8").strip()

    sbcp = int(sbcp) if sbcp else 0
    dbcp = int(dbcp) if dbcp else 0

    return sbcp, dbcp


def get_record_length_and_type(file: BinaryIO) -> Tuple[int, str]:
    """Get record length and its type.

    Parameters
    ----------
    file : BinaryIO.
        File-like object representing the IXF file.

    Returns
    -------
    Tuple[int, str]
        record length, record type
    """
    recl: int = int(file.read(6))
    rect: str = file.read(1).decode("utf-8")
    return recl, rect


def deltalake_fix_ns_timestamps(schema: pa.Schema) -> pa.Schema:
    """Fix issue with timestamps in deltalake.

    Deltalake has issue with timestamps in nanoseconds and it does not yet
    support it, so this function changes the pyarrow timestamp datatype
    in nanoseconds to microseconds. pyarrow timestamp datatype in microseconds
    is supported.

    Parameters
    ----------
    schema : Schema
        Pyarrow schema

    Returns
    -------
    Schema:
        Pyarrow schema with fix
    """
    for i, f in enumerate(schema):
        if f.type == pa.timestamp("ns"):
            new_field = pa.field(f.name, pa.timestamp("us"))
            schema = schema.set(i, new_field)
    return schema


def deltalake_fix_time(schema: pa.Schema) -> pa.Schema:
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
    schema : Schema
        Pyarrow schema

    Returns
    -------
    Schema
        Pyarrow schema with the fix.
    """
    time_datatypes = [
        pa.time64("ns"),
        pa.time64("us"),
        pa.time32("ms"),
        pa.time32("s")
    ]
    for i, f in enumerate(schema):
        if f.type in time_datatypes:
            new_field = pa.field(f.name, pa.string())
            schema = schema.set(i, new_field)
    return schema


def apply_schema_fixes(schema: pa.Schema) -> pa.Schema:
    """Apply all fixes on pyarrow schema to adapt to deltalake.

    Fixes issues in deltalake support for nanoseconds unit for time and
    timestamp datatype.

    Parameters
    ----------
    schema : Schema
        Pyarrow schema

    Returns
    -------
    Schema:
        Pyarrow schema with all fixes
    """

    fixes = [deltalake_fix_ns_timestamps, deltalake_fix_time]
    for fix in fixes:
        schema = fix(schema)
    return schema


def pyarrow_record_batches(
    data: Iterable[Dict], pyarrow_schema: pa.Schema, batch_size: int = 10000
) -> Iterable[pa.RecordBatch]:
    """Creates an Iterable of pyarrow record batches.

    Parameters
    ----------
    data : Iterable
        IXF data.
    pyarrow_schema : Schema
        Pyarrow schema.
    batch_size : int
        Number of rows to extract before writing to the parquet file.
        It is used for memory optimization.

    Yields
    ------
    RecordBatch
        Pyarrow record batch.
    """
    for batch in get_array_batch(data, size=batch_size):
        data = [pa.array(v) for v in batch.values()]
        pa_record_batch = pa.record_batch(data=data, schema=pyarrow_schema)
        yield pa_record_batch


def decode_field(field: str, cp: int, cpt: Literal["s", "d"] = "s"):
    """Try to decode the field using the provided codepage.

    Parameters
    ----------
    field : str
        Field containing data
    cp : int
        IBM code page
    cpt : Literal["s", "d"]
        Defaults to `s` which means single byte and `d` means double bytes

    Returns
    -------
    str:
        Decoded field
    """
    if cpt not in ["s", "d"]:
        raise ValueError("Either `s` for single bytes or `d` for double bytes")

    try:
        return field.decode(f"cp{cp}")
    except UnicodeDecodeError:
        logger.debug("Trying cp437 encoding")
        try:
            return field.decode("cp437")
        except UnicodeDecodeError:
            try:
                logger.debug("Trying to detect the encoding")
                _encoding = chardet.detect(field, True)["encoding"]
                return field.decode(_encoding)
            except UnicodeDecodeError as err:
                logger.debug(f"Detected encoding fails: {err}")
                try:
                    if cpt == "s":
                        logger.debug("Trying utf-8 encoding")
                        return field.decode("utf-8")
                    else:
                        try:
                            logger.debug("Trying utf-16 encoding")
                            return field.decode("utf-16")
                        except UnicodeDecodeError:
                            logger.debug("Trying utf-32 encoding")
                            return field.decode("utf-32")
                except UnicodeDecodeError:
                    logger.debug("Alert: eventual data loss, please provide encoding !")
                    return field.decode(f"cp{cp}", errors="ignore")
