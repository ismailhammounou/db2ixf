# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/).

<!-- release notes start -->

## [0.14.0](https://github.com/ismailhammounou/db2ixf/tree/0.14.0) - 2024-03-03

### Added

- Improve the way we get the optimal batch
  size [db2ixf-71](https://github.com/ismailhammounou/db2ixf/issues/71)

### Changed

- Rename and refactor some parts of the
  code [db2ixf-70](https://github.com/ismailhammounou/db2ixf/issues/70)

## [0.13.4](https://github.com/ismailhammounou/db2ixf/tree/0.13.4) - 2024-02-23

### Fixed

- bug: pyarrow.lib.ArrowTypeError: Expected bytes, got a 'datetime.time'
  object [db2ixf-69](https://github.com/ismailhammounou/db2ixf/issues/69)

## [0.13.3](https://github.com/ismailhammounou/db2ixf/tree/0.13.3) - 2024-02-22

### Fixed

- bug when using seek on Remote
  FileSystem [db2ixf-68](https://github.com/ismailhammounou/db2ixf/issues/68)

## [0.13.2](https://github.com/ismailhammounou/db2ixf/tree/0.13.2) - 2024-02-22

### Fixed

- bug in calculating file size when file opened by a non local file
  system [db2ixf-67](https://github.com/ismailhammounou/db2ixf/issues/67)

## [0.13.1](https://github.com/ismailhammounou/db2ixf/tree/0.13.1) - 2024-02-21

### Fixed

- to_csv does not write the
  header [db2ixf-66](https://github.com/ismailhammounou/db2ixf/issues/66)

## [0.13.0](https://github.com/ismailhammounou/db2ixf/tree/0.13.0) - 2024-02-21

### Added

- Change default batch size to decrease IO in some use
  cases [db2ixf-62](https://github.com/ismailhammounou/db2ixf/issues/62)
- Improve decimal
  collector [db2ixf-64](https://github.com/ismailhammounou/db2ixf/issues/64)

## [0.12.1](https://github.com/ismailhammounou/db2ixf/tree/0.12.1) - 2024-02-16

### Fixed

- Fix UnboundLocalError
  error [db2ixf-61](https://github.com/ismailhammounou/db2ixf/issues/61)

## [0.12.0](https://github.com/ismailhammounou/db2ixf/tree/0.12.0) - 2024-02-16

### Added

- Add doc about corrupted data and how it is
  handle [db2ixf-55](https://github.com/ismailhammounou/db2ixf/issues/55)
- improve
  documentation [db2ixf-59](https://github.com/ismailhammounou/db2ixf/issues/59)
- Add garbage collection and try some workarounds to avoid memory
  leaks [db2ixf-60](https://github.com/ismailhammounou/db2ixf/issues/60)

## [0.11.0](https://github.com/ismailhammounou/db2ixf/tree/0.11.0) - 2024-02-15

### Added

- Add support for
  jsonline [db2ixf-56](https://github.com/ismailhammounou/db2ixf/issues/56)

### Changed

- Refactor code to avoid memory
  leaks [db2ixf-58](https://github.com/ismailhammounou/db2ixf/issues/58)

## [0.10.2](https://github.com/ismailhammounou/db2ixf/tree/0.10.2) - 2024-02-13

### Fixed

- Handle division by zero when calculating number of
  rows [db2ixf-54](https://github.com/ismailhammounou/db2ixf/issues/54)

## [0.10.1](https://github.com/ismailhammounou/db2ixf/tree/0.10.1) - 2024-02-09

### Fixed

- Fix error when checking data corruption rate against accepted
  one [db2ixf-53](https://github.com/ismailhammounou/db2ixf/issues/53)

## [0.10.0](https://github.com/ismailhammounou/db2ixf/tree/0.10.0) - 2024-02-09

### Added

- Raise error in case of more than x% of corrupted extracted
  data [db2ixf-52](https://github.com/ismailhammounou/db2ixf/issues/52)

### Changed

- Refactor code and delete some
  code [db2ixf-50](https://github.com/ismailhammounou/db2ixf/issues/50)
- Change parse to a generator to optimize the memory and let user more
  freedom [db2ixf-51](https://github.com/ismailhammounou/db2ixf/issues/51)

### Fixed

- Fix error with float collector unpack requires a buffer of 8
  bytes [db2ixf-49](https://github.com/ismailhammounou/db2ixf/issues/49)

## [0.9.0](https://github.com/ismailhammounou/db2ixf/tree/0.9.0) - 2024-02-01

### Added

- Add support to error handling when facing UnicodeDecoding
  errors [db2ixf-48](https://github.com/ismailhammounou/db2ixf/issues/48)

### Fixed

- Wrong alias of cp1252 to
  latin-1 [db2ixf-47](https://github.com/ismailhammounou/db2ixf/issues/47)

## [0.8.0](https://github.com/ismailhammounou/db2ixf/tree/0.8.0) - 2024-01-29

### Added

- Add support for VARGRAPHIC data
  type [db2ixf-45](https://github.com/ismailhammounou/db2ixf/issues/45)

## [0.7.1](https://github.com/ismailhammounou/db2ixf/tree/0.7.1) - 2023-11-24

### Fixed

- Fix TypeError: 'type' object is not
  subscriptable [db2ixf-44](https://github.com/ismailhammounou/db2ixf/issues/44)

## [0.7.0](https://github.com/ismailhammounou/db2ixf/tree/0.7.0) - 2023-11-03

### Changed

- Disable using large datatypes by default and enable schema_overwrite by
  default [db2ixf-43](https://github.com/ismailhammounou/db2ixf/issues/43)

## [0.6.0](https://github.com/ismailhammounou/db2ixf/tree/0.6.0) - 2023-11-03

### Changed

- Add more arguments to deltalake output to control schema and larger
  datatypes [db2ixf-40](https://github.com/ismailhammounou/db2ixf/issues/40)

### Fixed

- Fix bug in blob_collector and
  binary_collector [db2ixf-39](https://github.com/ismailhammounou/db2ixf/issues/39)
- Improve json encoder to handle binary
  data [db2ixf-41](https://github.com/ismailhammounou/db2ixf/issues/41)

## [0.5.1](https://github.com/ismailhammounou/db2ixf/tree/0.5.1) - 2023-10-31

### Fixed

- Fix error with
  blob_collector [db2ixf-38](https://github.com/ismailhammounou/db2ixf/issues/38)

## [0.5.0](https://github.com/ismailhammounou/db2ixf/tree/0.5.0) - 2023-10-26

### Added

- Add support for longvarchar ixf
  datatype [db2ixf-37](https://github.com/ismailhammounou/db2ixf/issues/37)

## [0.4.0](https://github.com/ismailhammounou/db2ixf/tree/0.4.0) - 2023-10-20

### Changed

- Refactor code so internals of the package can be used
  easily [db2ixf-35](https://github.com/ismailhammounou/db2ixf/issues/35)
- Refactor code, format it and get rid of unused variables
  ...etc [db2ixf-36](https://github.com/ismailhammounou/db2ixf/issues/36)

## [0.3.1](https://github.com/ismailhammounou/db2ixf/tree/0.3.1) - 2023-09-28

### Added

- Add documentation for
  deltalake [db2ixf-34](https://github.com/ismailhammounou/db2ixf/issues/34)
- Expose pyarrow record batches output so can be used with
  polars/deltalake [db2ixf-31](https://github.com/ismailhammounou/db2ixf/issues/31)
- Add doc about pyarrow record batch
  output [db2ixf-32](https://github.com/ismailhammounou/db2ixf/issues/32)
- add support for
  deltalake [db2ixf-33](https://github.com/ismailhammounou/db2ixf/issues/33)

## [0.2.1](https://github.com/ismailhammounou/db2ixf/tree/0.2.1) - 2023-06-21

### Added

- Add ixf sample data (
  db2) [db2ixf-25](https://github.com/ismailhammounou/db2ixf/issues/25)
- Add more unit tests to improve
  coverage [db2ixf-26](https://github.com/ismailhammounou/db2ixf/issues/26)
- Add tests in CI
  pipeline [db2ixf-27](https://github.com/ismailhammounou/db2ixf/issues/27)

### Changed

- Improve ibm codecs
  mapping [db2ixf-28](https://github.com/ismailhammounou/db2ixf/issues/28)

### Fixed

- fix issues with some data type
  collector [db2ixf-29](https://github.com/ismailhammounou/db2ixf/issues/29)

## [0.2.0](https://github.com/ismailhammounou/db2ixf/tree/0.2.0) - 2023-06-17

### Added

- Add unit tests [db2ixf-3](https://github.com/ismailhammounou/db2ixf/issues/3)
- Add ibm encoding to use on the fly by reading ixf
  file [db2ixf-23](https://github.com/ismailhammounou/db2ixf/issues/23)

### Changed

- improve CLI and adapt
  it [db2ixf-24](https://github.com/ismailhammounou/db2ixf/issues/24)

### Removed

- Delete encoding because IXF file contains the
  encoding [db2ixf-20](https://github.com/ismailhammounou/db2ixf/issues/20)
- Drop support for python
  3.7 [db2ixf-22](https://github.com/ismailhammounou/db2ixf/issues/22)

## [0.1.7](https://github.com/ismailhammounou/db2ixf/tree/0.1.7) - 2023-06-06

### Added

- Add support for CLOB data
  type [db2ixf-16](https://github.com/ismailhammounou/db2ixf/issues/16)
- Add support for BLOB data
  type [db2ixf-17](https://github.com/ismailhammounou/db2ixf/issues/17)
- Add support for binary data
  type [db2ixf-19](https://github.com/ismailhammounou/db2ixf/issues/19)

### Changed

- Improve
  documentation [db2ixf-18](https://github.com/ismailhammounou/db2ixf/issues/18)

## [0.1.6](https://github.com/ismailhammounou/db2ixf/tree/0.1.6) - 2023-06-05

### Fixed

- Fix bug with parquet_version param default value and pass it to pyarrow
  parquet
  writer [db2ixf-15](https://github.com/ismailhammounou/db2ixf/issues/15)

## [0.1.5](https://github.com/ismailhammounou/db2ixf/tree/0.1.5) - 2023-06-05

### Added

- Support of floating point data
  type [db2ixf-14](https://github.com/ismailhammounou/db2ixf/issues/14)

## [0.1.4](https://github.com/ismailhammounou/db2ixf/tree/0.1.4) - 2023-06-01

### Changed

- Improve ci and fix
  issues [db2ixf-12](https://github.com/ismailhammounou/db2ixf/issues/12)
- Improve ci-cd [db2ixf-2](https://github.com/ismailhammounou/db2ixf/issues/2)

## [0.1.3](https://github.com/ismailhammounou/db2ixf/tree/0.1.3) - 2023-05-31

### Fixed

- Fix issue with gh pages
  [db2ixf-11](https://github.com/ismailhammounou/db2ixf/issues/11)

## [0.1.2](https://github.com/ismailhammounou/db2ixf/tree/0.1.2) - 2023-05-31

### Fixed

- Fix issues in ci for gh-pages
  generation [db2ixf-10](https://github.com/ismailhammounou/db2ixf/issues/10)

## [0.1.1](https://github.com/ismailhammounou/db2ixf/tree/0.1.1) - 2023-05-31

### Added

- Add ci for github
  pages [db2ixf-9](https://github.com/ismailhammounou/db2ixf/issues/9)

### Changed

- Update documentation: CLI
  doc [db2ixf-4](https://github.com/ismailhammounou/db2ixf/issues/4)
- Improve
  documentation [db2ixf-7](https://github.com/ismailhammounou/db2ixf/issues/7)
- Prepare Mkdocs in order to publish in
  gh-pages [db2ixf-8](https://github.com/ismailhammounou/db2ixf/issues/8)

## [0.1.0](https://github.com/ismailhammounou/db2ixf/tree/0.1.0) - 2023-05-29

### Added

- Add IXF Parser [db2ixf-1](https://github.com/ismailhammounou/db2ixf/issues/1)
