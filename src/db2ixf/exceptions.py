# coding=utf-8
"""Custom exceptions for IXF parsing."""


class NotValidColumnDescriptorException(Exception):
    """
    Exception raised when encountering a non valid column descriptor.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-record-types)
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnknownDataTypeException(Exception):
    """
    Exception raised when encountering an unknown data type.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotValidDataPrecisionException(Exception):
    """
    Exception raised when encountering a non valid data precision.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class ExceedingDefinedMaximumLengthException(Exception):
    """
    Exception raised when encountering an object length exceeds the defined
    maximum length.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class LargeObjectLengthException(Exception):
    """
    Exception raised when encountering a large object length exceeding the
    maximum length.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BinaryLengthException(Exception):
    """
    Exception raised when encountering binary data type with a length exceeding
    the maximum length.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CharLengthException(Exception):
    """
    Exception raised when encountering char data type with a length exceeding
    the maximum length.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class VarCharLengthException(Exception):
    """
    Exception raised when encountering varchar data type with a length
    exceeding the maximum length.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class CLOBCodePageException(Exception):
    """
    Exception raised when encountering CLOB data type where SBCP and DBCP are
    simultaneously equal to 0

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class BlobBinaryStringException(Exception):
    """Exception raised when encountering a data type different of binary string
    which occurs when single byte code page equals to 0 but we re not getting
    a binary string but an other type like character string.

    Read the
    [doc](https://www.ibm.com/docs/en/db2/11.5?topic=format-pcixf-data-types).
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
