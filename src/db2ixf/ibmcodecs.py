# coding=utf-8
"""Add new codecs that maps ibm code pages to python encodings."""
import codecs


class UTF32BECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_be_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_be_decode(input, errors, True)


def ibm_utf_32_be(name):
    aliases = ['ibm1232', '1232', 'cp1232', 'ibm1233', '1233', 'cp1233']
    if name.lower() in aliases:
        return UTF32BECodec()


class UTF32LECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_le_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_le_decode(input, errors, True)


def ibm_utf_32_le(name):
    aliases = ['ibm1234', '1234', 'cp1234', 'ibm1235', '1235', 'cp1235']
    if name.lower() in aliases:
        return UTF32LECodec()


class UTF32Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_decode(input, errors, True)


def ibm_utf_32(name):
    aliases = ['ibm1236', '1236', 'cp1236', 'ibm1237', '1237', 'cp1237']
    if name.lower() in aliases:
        return UTF32Codec()


class UTF16BECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_be_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_be_decode(input, errors, True)


def ibm_utf_16_be(name):
    aliases = ['ibm1200', '1200', 'cp1200', 'ibm1201', '1201', 'cp1201']
    if name.lower() in aliases:
        return UTF16BECodec()


class UTF16LECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_le_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_le_decode(input, errors, True)


def ibm_utf_16_le(name):
    aliases = ['ibm1202', '1202', 'cp1202', 'ibm1203', '1203', 'cp1203']
    if name.lower() in aliases:
        return UTF16LECodec()


class UTF16Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_decode(input, errors, True)


def ibm_utf_16(name):
    aliases = ['ibm1204', '1204', 'cp1204', 'ibm1205', '1205', 'cp1205']
    if name.lower() in aliases:
        return UTF16Codec()


class UTF8Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_8_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_8_decode(input, errors, True)


def ibm_utf_8(name):
    aliases = ['ibm1208', '1208', 'cp1208', 'ibm1209', '1209', 'cp1209']
    if name.lower() in aliases:
        return UTF8Codec()
