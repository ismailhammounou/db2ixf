To begin using the IXF Parser package, follow the installation instructions
below.

## Installation

Ensure that you have set up and activated a Python virtual environment. Then,
use the following command to install the package:

```bash
pip install db2ixf
```

## Examples

Below are examples demonstrating how to use the IXF Parser package:

#### Parsing an IXF File

You can parse an IXF file by providing a file-like object or a path to the file.
Here's an example using a file-like object:

```python
# coding=utf-8
from pathlib import Path
from db2ixf.ixf import IXFParser

path = Path('Path/to/IXF/FILE/XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    rows = parser.parse()
    for row in rows:
        print(row)
```

In this example, the `IXFParser` is initialized with a file-like object `f`, and
the `parse` method is used to retrieve the parsed rows as a list of
dictionaries.

#### Converting to JSON

You can convert the parsed data to JSON format and save it to a file. Here's an
example:

```python
# coding=utf-8
from pathlib import Path
from db2ixf.ixf import IXFParser

path = Path('Path/to/IXF/FILE/XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('Path/To/Output/YYY.json')
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        parser.to_json(output_file)
```

In this example, the parsed data is converted to JSON format using the
`to_json` method and saved to the specified output file.

#### Converting to JSONLINE

You can convert the parsed data to JSONLINE format and save it to a file. Here's
an example:

```python
# coding=utf-8
from pathlib import Path
from db2ixf.ixf import IXFParser

path = Path('Path/to/IXF/FILE/XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('Path/To/Output/YYY.jsonl')
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        parser.to_jsonline(output_file)
```

In this example, the parsed data is converted to JSONLINE format using the
`to_jsonline` method and saved to the specified output file.

#### Converting to CSV

You can also convert the parsed data to CSV format and save it to a file. Here's
an example:

```python
# coding=utf-8
import pathlib
from db2ixf.ixf import IXFParser

path = pathlib.Path('Path/to/IXF/FILE/XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = pathlib.Path('Path/To/Output/YYY.csv')
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        parser.to_csv(output_file, sep='#')
```

In this example, the parsed data is converted to CSV format using the `to_csv`
method and saved to the specified output file. The `sep` parameter specifies the
separator/delimiter to be used in the CSV file.

#### Converting to Parquet

If you prefer to store the parsed data in Parquet format, you can use the
following example:

```python
# coding=utf-8
from pathlib import Path
from db2ixf.ixf import IXFParser

path = Path('Path/to/IXF/FILE/XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('Path/To/Output/YYY.parquet')
    with open(output_path, mode='wb') as output_file:
        parser.to_parquet(output_file)
```

In this example, the parsed data is converted to Parquet format using
the `to_parquet` method and saved to the specified output file.

#### Converting to Deltalake

If you prefer to store the parsed data in Deltalake format, you can use the
following example:

```python
# coding=utf-8
from pathlib import Path
from db2ixf.ixf import IXFParser

path = Path('Path/to/IXF/FILE/XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('Path/To/Output/Table')
    parser.to_deltalake(output_path)
```

In this example, the parsed data is converted to Deltalake format using
the `to_deltalake` method and saved to the specified output path.

You can also use a string but Path is better in case you work on a local
filesystem. When we use a string, it is often for a remote storage and in this
case you can either use filesystem argument or let `deltalake` package infer it
from the uri.

---

The IXF Parser package provides flexibility in terms of input and output
options, allowing you to easily parse and process IXF files according to your
needs.

#### Precautions

There are cases where the parsing can fail and sometimes can lead to data loss:

1. Completely corrupted ixf file: It is usually an extraction issue.
2. Partially corrupted ixf file, it contains some corrupted Rows/Lines that the
   parser can not parse.
    1. Parser calculates rate of corrupted rows then compares it to an accepted
       rate of corrupted rows which you can set by this environment variable
       `DB2IXF_ACCEPTED_CORRUPTION_RATE`(int = 1)%.
    2. If the rate of corrupted rows is bigger than the accepted rate the parser
       raises an exception.
3. Unsupported data type : please contact the owners/maintainers/contributors so
   you can get help otherwise any PR is welcomed.

???+ danger "4. case: encoding issues"

    Parsing can lead to data loss in case the found or the detected encoding is 
    not able to decode some extracted fields/columns. 
    
    Parser tries to decode using:
        
        1. The found encoding (found in the column record)
        
        2. Other encodings like cp437
        
        3. The detected encoding using a third party package (chardet)
        
        4. Encodings like utf-8 and utf-32
        
        5. Ignore errors which can lead to data loss !
    
    Before use the package in production, try to test in debug mode so you can
    detect data loss.

## CLI

Start with this:

``` bash title="Bash Command"
db2ixf --help
```

``` bash title="Command Result"

 Usage: db2ixf [OPTIONS] COMMAND [ARGS]...

 A command-line tool (CLI) for parsing and converting IXF (IBM DB2 
 Import/Export Format) files to various formats such as JSON, JSONLINE, CSV and 
 Parquet. Easily parse and convert IXF files to meet your data processing needs.

+- Options -------------------------------------------------------------------+
| --version             -v        Show the version of the CLI.                |
| --install-completion            Install completion for the current shell.   |
| --show-completion               Show completion for the current shell, to   |
|                                 copy it or customize the installation.      |
| --help                          Show this message and exit.                 |
+-----------------------------------------------------------------------------+
+- Commands ------------------------------------------------------------------+
| csv      Parse ixf FILE and convert it to a csv OUTPUT.                     |
| json     Parse ixf FILE and convert it to a json OUTPUT.                    |
| jsonline     Parse ixf FILE and convert it to a jsonline OUTPUT.            |
| parquet  Parse ixf FILE and convert it to a parquet OUTPUT.                 |
+-----------------------------------------------------------------------------+

 Made with heart :D

```

The `db2ixf` command-line tool (CLI) is used for parsing and converting IXF (IBM
DB2 Import/Export Format) files to various formats such as JSON, JSONLINE, CSV
and Parquet. It provides an easy way to parse and convert IXF files to meet your
data processing needs.

**Options**:

- `--version` or `-v`: Show the version of the CLI.
- `--install-completion`: Install completion for the current shell.
- `--show-completion`: Show completion for the current shell, to copy it or
  customize the installation.
- `--help`: Show this message and exit.

**Commands**:

- `csv`: Parse the specified `ixf` FILE and convert it to a CSV OUTPUT.
- `json`: Parse the specified `ixf` FILE and convert it to a JSON OUTPUT.
- `jsonline`: Parse the specified `ixf` FILE and convert it to a JSONLINE
  OUTPUT.
- `parquet`: Parse the specified `ixf` FILE and convert it to a Parquet OUTPUT.

This CLI tool is made with love ! ❤️

### Examples

There are 4 commands and each one is related to an output format. ``db2ixf``
supports only ``json``, ``jsonline``, ``csv`` and ``parquet``.

=== "json"

    ```bash
    db2ixf json "Path/to/IXF/file.IXF"
    ```

=== "jsonline"

    ```bash
    db2ixf jsonline "Path/to/IXF/file.IXF"
    ```

=== "csv"

    ```bash
    db2ixf csv "Path/to/IXF/file.IXF"
    ```

=== "parquet"

    ```bash
    db2ixf parquet "Path/to/IXF/file.IXF"
    ```

!!! Note

    In the example above, the output file will be created in directory where you
    launch the command. The name of output file will be the same as the ixf 
    file.

These are complete examples for all the commands:

=== "json"

    ```bash
    db2ixf json -vvv "Path/to/IXF/file.IXF" "Path/to/OUTPUT/file.json"
    ```

=== "jsonline"

    ```bash
    db2ixf jsonline -vvv "Path/to/IXF/file.IXF" "Path/to/OUTPUT/file.jsonl"
    ```

=== "csv"

    ```bash
    db2ixf csv -vvv --sep "!" "Path/to/IXF/file.IXF" "Path/to/OUTPUT/file.csv"
    ```

=== "parquet"

    ```bash
    db2ixf parquet -vvv --version "1.0" --batch-size 4000 "Path/to/IXF/file.IXF" "Path/to/OUTPUT/file.parquet"
    ```

!!! tip

    Before using one of the examples, please, try `db2ixf <command> --help` to
    get details on how to use the command.

!!! info

    CLI does not support the deltalake format. In case, you need support
    please create an issue in Github.
