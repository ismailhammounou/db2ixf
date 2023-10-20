# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres
to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

This project uses [*towncrier*](https://towncrier.readthedocs.io/).

<!-- release notes start -->

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
