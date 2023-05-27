## Story

### Definition

**IXF** stands for "IBM eXchange Format," and it is a file format used by 
IBM's DB2 database system for data import and export operations. 
The IXF format provides a standardized and efficient way to exchange data 
between DB2 databases or between DB2 and other systems.

### Context

At work, we encountered the need to extract data from our DB2 database 
for analysis purposes. However, obtaining the data in a usable format 
proved to be a challenge. The IT department provided us with IXF files 
containing the exported data, but we required a solution to parse and 
process this data effectively.

### Solution

To address this issue, I developed a package that simplifies the parsing 
of IXF files. This package builds upon existing open-source projects, 
which proved to be valuable resources. By leveraging these projects, 
I was able to create a package that streamlines the parsing of IXF files 
and offers various output options.

### Package Features

The IXF Parser package offers the following features:

1. **Parsing IXF Files**: The package allows for the parsing of IXF files, 
extracting the rows of data contained within.

2. **Conversion to Multiple Formats**: The parsed data can be converted to 
different formats, including JSON, CSV, and Parquet.

3. **Support for File-Like Objects**: The package supports file-like objects 
as input, enabling the direct parsing of IXF data from file objects.

4. **Minimal Dependency**: The package has only 2 dependencies, pyarrow and 
   typer, which are automatically installed alongside the package.

5. **CLI**: Command line tool called `db2ixf`.

## Getting Started

To begin using the IXF Parser package, follow the installation 
instructions below.

### Installation

Ensure that you have set up and activated a Python virtual environment. 
Then, use the following command to install the package:

```bash
pip install db2ixf
```

### Examples

Below are examples demonstrating how to use the IXF Parser package:

#### Parsing an IXF File

You can parse an IXF file by providing a file-like object or a path to 
the file. Here's an example using a file-like object:

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

In this example, the `IXFParser` is initialized with a file-like object `f`, 
and the `parse` method is used to retrieve the parsed rows as a list of 
dictionaries.

#### Converting to JSON

You can convert the parsed data to JSON format and save it to a file. 
Here's an example:

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

#### Converting to CSV

You can also convert the parsed data to CSV format and save it to a file. 
Here's an example:

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
method and saved to the specified output file. The `sep` parameter specifies 
the separator/delimiter to be used in the CSV file.

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

The IXF Parser package provides flexibility in terms of input and 
output options, allowing you to easily parse and process IXF files 
according to your needs.