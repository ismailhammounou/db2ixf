# Story

## Definition

**IXF** stands for "IBM eXchange Format," and it is a file format used by IBM's
DB2 database system for data import and export operations. The IXF format
provides a standardized and efficient way to exchange data between DB2 databases
or between DB2 and other systems.

## Context

At work, we encountered the need to extract data from our DB2 database for
analysis purposes. However, obtaining the data in a usable format proved to be a
challenge. The IT department provided us with IXF files containing the exported
data, but we required a solution to parse and process this data effectively.

## Solution

To address this issue, I developed a package that simplifies the parsing of IXF
files. This package builds upon existing open-source projects, which proved to
be valuable resources. By leveraging these projects, I was able to create a
package that streamlines the parsing of IXF files and offers various output
options.

## Package Features

The IXF Parser package offers the following features:

1. **Parsing IXF Files**: The package allows for the parsing of IXF files,
   extracting the rows of data contained within.

2. **Conversion to Multiple Formats**: The parsed data can be converted to
   different formats, including JSON, CSV, and Parquet.

3. **Support for File-Like Objects**: The package supports file-like objects as
   input, enabling the direct parsing of IXF data from file objects.

4. **Minimal dependencies**: The package has only 3 dependencies (pyarrow, typer
   and ebcdic) which are automatically installed alongside the package.

5. **CLI**: Command line tool called `db2ixf`.