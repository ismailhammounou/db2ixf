# coding=utf-8
"""Custom exceptions for IXF parsing."""


class NotValidColumnDescriptorException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class UnknownDataTypeException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)


class NotValidDataPrecisionException(Exception):
    def __init__(self, message):
        self.message = message
        super().__init__(self.message)
