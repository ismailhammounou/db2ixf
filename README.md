[![Language](https://img.shields.io/pypi/pyversions/db2ixf?color=ffde57&logo=python&style=for-the-badge)](https://www.python.org/)
[![License](https://img.shields.io/pypi/l/db2ixf?color=3775A9&style=for-the-badge&logo=unlicense)](https://www.gnu.org/licenses/agpl-3.0)

[![Pipeline](https://img.shields.io/github/actions/workflow/status/ismailhammounou/db2ixf/db2ixf.yml?branch=main&style=for-the-badge&logo=gitHub-actions)](https://github.com/ismailhammounou/db2ixf/actions/workflows/db2ixf.yml)
[![Release](https://img.shields.io/github/v/release/ismailhammounou/db2ixf?display_name=tag&sort=semver&style=for-the-badge&logo=semver)](https://github.com/ismailhammounou/db2ixf/releases/latest)
[![Pypi](https://img.shields.io/pypi/v/db2ixf?color=3775A9&logo=pypi&style=for-the-badge)](https://pypi.org/project/db2ixf/)

[![Downloads](https://img.shields.io/pypi/dm/db2ixf?style=for-the-badge)](https://pypi.org/project/db2ixf/)
[![Contributors](https://img.shields.io/github/contributors/ismailhammounou/db2ixf?style=for-the-badge)](https://github.com/ismailhammounou/db2ixf/graphs/contributors)


[![Documentation](https://img.shields.io/badge/here-here?style=for-the-badge&logo=book&label=documentation&color=purple
)](https://ismailhammounou.github.io/db2ixf/)



# DB2IXF Parser

<div align="center">
  <img src="https://github.com/ismailhammounou/db2ixf/blob/main/resources/images/db2ixf-logo.png?raw=true" alt="Logo" width="300" height="300">
</div>

DB2IXF parser is an open-source python package that simplifies the parsing and
processing of IBM Integration eXchange Format (IXF) files. IXF is a file format
used by IBM's DB2 database system for data import and export operations. This
package provides a streamlined solution for extracting data from IXF files and
converting it to various formats, including JSON, CSV, Parquet and Deltalake.

## Features

- **Parse IXF files**: The package allows you to parse IXF files and extract the
  rows of data stored within them.
- **Convert to multiple formats**: The parsed data can be easily converted to
  JSON, CSV, or Parquet format, providing flexibility for further analysis and
  integration with other systems.
- **Support for file-like objects**: IXF Parser supports file-like objects as
  input, enabling direct parsing of IXF data from file objects, making it
  convenient for handling large datasets without the need for intermediate file
  storage.
- **Minimal dependencies**: The package has only 4 dependencies (deltalake,
  pyarrow, typer and ebcdic) which are automatically installed alongside the
  package.
- **CLI**: command line tool called ``db2ixf`` comes with the package. (_Does
  not support Deltalake format_)

## Hypothesis

- **One** IXF file contains **One** table.

## Getting Started

### Installation

You can install DB2 IXF Parser using pip:

```bash
pip install db2ixf
```

### Usage

Here are some examples of how to use DB2 IXF Parser:

#### CLI

Start with this:

```bash
db2ixf --help
```

Result:

```
 Usage: db2ixf [OPTIONS] COMMAND [ARGS]...

 A command-line tool (CLI) for parsing and converting IXF (IBM DB2 Import/Export 
 Format) files to various formats such as JSON, CSV, and Parquet. Easily parse 
 and convert IXF files to meet your data processing needs.

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
| parquet  Parse ixf FILE and convert it to a parquet OUTPUT.                 |
+-----------------------------------------------------------------------------+

 Made with heart :D

```

#### Parsing an IXF file

```python
# coding=utf-8
from pathlib import Path
from db2ixf import IXFParser

path = Path('path/to/IXF/file.XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    rows = parser.parse()
    for row in rows:
        print(row)
```

#### Converting to JSON

```python
# coding=utf-8
from pathlib import Path
from db2ixf import IXFParser

path = Path('path/to/IXF/file.XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('path/to/output/file.json')
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        parser.to_json(output_file)
```

#### Converting to CSV

```python
# coding=utf-8
from pathlib import Path
from db2ixf import IXFParser

path = Path('path/to/IXF/file.XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('path/to/output/file.csv')
    with open(output_path, mode='w', encoding='utf-8') as output_file:
        parser.to_csv(output_file)
```

#### Converting to Parquet

```python
# coding=utf-8
from pathlib import Path
from db2ixf import IXFParser

path = Path('path/to/IXF/file.XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = Path('path/to/output/file.parquet')
    with open(output_path, mode='wb') as output_file:
        parser.to_parquet(output_file)
```

#### Converting to Deltalake

```python
# coding=utf-8
from pathlib import Path
from db2ixf import IXFParser

path = Path('path/to/IXF/file.XXX.IXF')
with open(path, mode='rb') as f:
    parser = IXFParser(f)
    output_path = 'path/to/output/'
    parser.to_deltalake(output_path)
```

For a detailed story and usage, please refer to the
[documentation](https://ismailhammounou.github.io/db2ixf/).

## Contributing

IXF Parser is actively seeking contributions to enhance its features and
reliability. Your participation is valuable in shaping the future of the
project.

We appreciate your feedback, bug reports, and feature requests. If you encounter
any issues or have ideas for improvement, please open an issue on the
[GitHub repository](https://github.com/ismailhammounou/db2ixf/issues).

For any questions or assistance during the contribution process, feel free to
reach out by opening an issue on the
[GitHub repository](https://github.com/ismailhammounou/db2ixf/issues).

Thank you for considering contributing to IXF Parser. Let's work together to
create a powerful and dependable tool for working with DB2's IXF files.

### Todo

- [ ] Search for contributors/maintainers/sponsors.
- [x] Add tests (Manual testing was done but need write unit tests).
- [x] Adding new collector for the floating point data type.
- [x] Adding new collectors for other ixf data types: binary ...etc.
- [ ] Improve documentation.
- [x] Add a CLI.
- [x] Improve CLI: output can be optional.
- [x] Add better ci-cd.
- [x] Improve Makefile.
- [x] ~~Support multiprocessing.~~
- [x] ~~Support archived inputs: only python not CLI ?~~
- [x] Add logging.
- [x] Add support for deltalake
- [x] Add support for pyarrow

## License

IXF Parser is released under the
[AGPL-3.0 License](https://github.com/ismailhammounou/db2ixf/blob/main/LICENSE).

## Support

If you encounter any issues or have questions about using IXF Parser, please
open an issue on the
[GitHub repository](https://github.com/ismailhammounou/db2ixf/issues). We will
do our best to address them promptly.

## Conclusion

IXF Parser offers a convenient solution for parsing and processing IBM DB2's IXF
files. With its ease of use and support for various output formats, it provides
a valuable tool for working with DB2 data. We hope that you find this package
useful in your data analysis and integration workflows.

Give it a try and let us know your feedback. Happy parsing!
