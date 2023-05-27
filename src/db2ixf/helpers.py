# coding=utf-8
"""Create helper function for schema generation and others."""
import pyarrow
from db2ixf.constants import IXF_DTYPES
from db2ixf.exceptions import NotValidDataPrecisionException
from typing import Generator, Dict


def get_pyarrow_schema(cols: list[dict]) -> dict[str, object]:
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
        'DATE': pyarrow.date32(),
        'TIME': pyarrow.time64('ns'),
        'TIMESTAMP': pyarrow.timestamp('ns'),
        'VARCHAR': pyarrow.string(),
        'CHAR': pyarrow.string(),
        'DECIMAL': pyarrow.decimal128(19),
        'BIGINT': pyarrow.int64(),
        'INTEGER': pyarrow.int32(),
        'SMALLINT': pyarrow.int16(),
    }

    schema = {}
    for c in cols:
        cname = c['IXFCNAME'].decode('utf-8').strip()
        ctype = int(c['IXFCTYPE'])
        dtype = mapper[IXF_DTYPES[ctype]]

        if ctype == 484:
            precision = int(c['IXFCLENG'][0:3])
            scale = int(c['IXFCLENG'][3:5])
            if scale == 0:
                dtype = pyarrow.int64()
            else:
                dtype = pyarrow.decimal128(precision, scale)

        if ctype == 392:
            fsp = int(c['IXFCLENG'])
            if fsp == 0:
                dtype = pyarrow.timestamp('s')
            elif 0 < fsp <= 3:
                dtype = pyarrow.timestamp('ms')
            elif 3 < fsp <= 6:
                dtype = pyarrow.timestamp('us')
            elif 6 < fsp <= 12:
                dtype = pyarrow.timestamp('ns')
            else:
                msg = f'Precision of the decimal column {cname} is not valid, it should be <= 12'
                raise NotValidDataPrecisionException(msg)

        schema[cname] = dtype

    return schema


def get_pandas_schema(cols: list[dict]):
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
        'DATE': 'datetime64[ns]',
        'TIME': 'datetime64[ns]',
        'TIMESTAMP': 'datetime64[ns]',
        'VARCHAR': object,
        'CHAR': object,
        'DECIMAL': 'float32',
        'BIGINT': 'int64',
        'INTEGER': 'int64',
        'SMALLINT': 'int64',
    }

    schema = {}
    for c in cols:
        cname = str(c['IXFCNAME'], encoding='utf-8').strip()
        ctype = int(c['IXFCTYPE'])
        dtype = mapper[IXF_DTYPES[ctype]]

        if ctype == 484:
            precision = int(c['IXFCLENG'][0:3])
            scale = int(c['IXFCLENG'][3:5])
            if scale == 0:
                dtype = 'int64'
            else:
                dtype = 'float32'

        schema[cname] = dtype

    return schema


def merge_dicts(dicts: list[dict]) -> dict[str, list]:
    """
    Merge a list of dictionaries into a single dictionary where each key is mapped
    to a list of its values.

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
    >>> ex = [{'key1': 'value1', 'key2': 'value2'}, {'key1': 'value3', 'key2': 'value4'}]
    >>> merge_dicts(ex)
    {'key1': ['value1', 'value3'], 'key2': ['value2', 'value4']}
    """

    result = {}

    for dictionary in dicts:
        for key, value in dictionary.items():
            result.setdefault(key, []).append(value)

    return result


def get_batch(generator: Generator, size: int = 500) -> Dict[str, list]:
    """Batch generator. It yields a batch of rows in a single dictionary.

    It gets a list of size '`size`' containing rows from the data source generator then merge all
    rows in one dictionary which is the yielded one.


    Parameters
    ----------
    generator : Generator
        Python generator that yields individual rows from the source data.
    size : int, optional
        Size of each batch (number of rows per batch). Default is 500.

    Yields
    ------
    Generator[List, None, None]
        A generator that yields batches of rows, where each batch is a list of rows.

    Examples
    --------
    Get a batch generator from a data generator and process the batches:

    >>> data_generator = some_data_generator  # Assuming yields rows  # noqa
    >>> batch_generator = get_batch(data_generator, size=100)

    >>> for b in batch_generator:
    ...     # Process the batch of rows
    ...     process_batch(b) # noqa

    Notes
    -----
    - The function accumulates rows until the number of rows reaches the specified `size`.
    - Once the accumulated rows reach the `size`, a batch is formed and yielded.
    - If there are remaining rows that do not form a complete batch, they are yielded as the last batch.
    - The `merge_dicts` function should be implemented separately and used to merge the rows into a single dictionary.
    """

    rows = []
    for i, row in enumerate(generator()):
        rows.append(row)
        if (i + 1) % size == 0:
            batch = merge_dicts(rows)
            yield batch
            rows = []

    # Yield the remaining rows as the last batch
    if rows:
        batch = merge_dicts(rows)
        yield batch
