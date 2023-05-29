[![Pipeline](https://github.com/ismailhammounou/db2ixf/actions/workflows/db2ixf.yml/badge.svg)](https://github.com/ismailhammounou/db2ixf/actions/workflows/db2ixf.yml)

# DB2IXF Parser


<img src="https://github.com/ismailhammounou/db2ixf/blob/main/resources/images/db2ixf-logo.png?raw=true" alt="Logo" style="display: block; margin: 0 auto;">


DB2IXF parser is an open-source python package that simplifies the parsing and
processing of IBM eXchange Format (IXF) files. IXF is a file format used by
IBM's DB2 database system for data import and export operations. This package
provides a streamlined solution for extracting data from IXF files and
converting it to various formats, including JSON, CSV, and Parquet.

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
- **Minimal dependencies**: The package has only 2 dependencies, pyarrow and
  typer, which are automatically installed alongside the package.
- **CLI**: command line tool called ``db2ixf`` comes with the package.

## Getting Started

### Installation

You can install DB2 IXF Parser using pip:

```bash
pip install db2ixf
```

### Usage

Here are some examples of how to use DB2 IXF Parser:

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

For detailed usage instructions, please refer to the
[documentation](https://github.com/ismailhammounou/db2ixf).

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
- [ ] Add tests (Manual testing was done but need write unit tests).
- [ ] Adding new collectors for other ixf data types: floating point ... etc.
- [ ] Improve documentation.
- [x] Add a CLI.
- [x] Improve CLI: output can be optional.
- [ ] Add better ci-cd.
- [ ] Improve Makefile.
- [ ] Support multiprocessing.
- [ ] Support archived inputs: only python not CLI ?
- [x] Add logging.

## License

IXF Parser is released under the
[AGPL-3.0 License](https://github.com/ismailhammounou/db2ixf/blob/main/LICENSE).

## Acknowledgements

IXF Parser was made possible by the contributions of several individuals. We
would like to acknowledge the following:

- [OpenAI](https://openai.com/): For documentation.

- [PyArrow](https://arrow.apache.org/): For the excellent library that enables
  efficient conversion to Parquet format.

- [Typer](https://typer.tiangolo.com/) : For the excellent tool helping to
  create CLI.

- [Contributors \& Users](https://github.com/ismailhammounou/db2ixf/graphs/contributors):
  For their valuable feedback, bug reports, and contributions to the project.

We are grateful for the support and collaboration that have helped shape the IXF
Parser package into what it is today.

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