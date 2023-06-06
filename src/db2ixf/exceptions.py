# coding=utf-8
"""Custom exceptions for IXF parsing."""


class NotValidColumnDescriptorException(Exception):
    """
    Exception raised when encountering a non valid column descriptor.

    Read the [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-record-types)
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnknownDataTypeException(Exception):
    """
    Exception raised when encountering an unknown data type.

    Read the [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotValidDataPrecisionException(Exception):
    """
    Exception raised when encountering a non valid data precision.

    Read the [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ExceedingDefinedMaximumLengthException(Exception):
    """
    Exception raised when encountering an object length exceeds the defined
    maximum length.

    Read the [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LargeObjectLengthException(Exception):
    """
    Exception raised when encountering a large object length exceeding the
    maximum length.

    Read the [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BinaryLengthException(Exception):
    """
    Exception raised when encountering a length exceeding the maximum length.

    Read the [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
