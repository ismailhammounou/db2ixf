# coding=utf-8
"""Custom exceptions for IXF parsing."""


class NotValidColumnDescriptorException(Exception):
    """
    Exception raised when encountering a non valid column descriptor.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnknownDataTypeException(Exception):
    """
    Exception raised when encountering an unknown data type.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotValidDataPrecisionException(Exception):
    """
    Exception raised when encountering a non valid data precision.
    """

    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
