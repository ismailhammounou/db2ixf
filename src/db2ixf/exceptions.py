# coding=utf-8
"""Custom exceptions for IXF parsing."""


class IXFParsingError(Exception):
    """Exception raised when facing issues with corrupted data of IXF file."""
    pass


class DataCollectorError(Exception):
    """Exception raised when facing issues with data collection
    from the IXF file. Read the doc:
    https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types
    """
    pass


class NotValidColumnDescriptorException(Exception):
    """Exception raised when encountering a
    non valid column descriptor. Read the doc:
    https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-record-types
    """
    pass


class UnknownDataTypeException(Exception):
    """Exception raised when encountering an
    unknown data type. Read the doc:
    https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types
    """
    pass


class NotValidDataPrecisionException(Exception):
    """Exception raised when encountering a
    non valid data precision. Read the doc
    https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types
    """
    pass
