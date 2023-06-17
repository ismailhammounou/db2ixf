# coding=utf-8
"""Add new codecs that maps ibm code pages to python encodings."""
import codecs


class UTF32BECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_be_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_be_decode(input, errors, True)


def ibm_utf_32_be(name):
    aliases = ['ibm1232', 'cp1232', 'ibm1233', 'cp1233']
    if name.lower() in aliases:
        return UTF32BECodec()


class UTF32LECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_le_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_le_decode(input, errors, True)


def ibm_utf_32_le(name):
    aliases = ['ibm1234', 'cp1234', 'ibm1235', 'cp1235']
    if name.lower() in aliases:
        return UTF32LECodec()


class UTF32Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_32_decode(input, errors, True)


def ibm_utf_32(name):
    aliases = ['ibm1236', 'cp1236', 'ibm1237', 'cp1237']
    if name.lower() in aliases:
        return UTF32Codec()


class UTF16BECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_be_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_be_decode(input, errors, True)


def ibm_utf_16_be(name):
    aliases = ['ibm1200', 'cp1200', 'ibm1201', 'cp1201']
    if name.lower() in aliases:
        return UTF16BECodec()


class UTF16LECodec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_le_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_le_decode(input, errors, True)


def ibm_utf_16_le(name):
    aliases = ['ibm1202', 'cp1202', 'ibm1203', 'cp1203']
    if name.lower() in aliases:
        return UTF16LECodec()


class UTF16Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_16_decode(input, errors, True)


def ibm_utf_16(name):
    aliases = ['ibm1204', 'cp1204', 'ibm1205', 'cp1205']
    if name.lower() in aliases:
        return UTF16Codec()


class UTF8Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.utf_8_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.utf_8_decode(input, errors, True)


def ibm_utf_8(name):
    aliases = ['ibm1208', 'cp1208', 'ibm1209', 'cp1209']
    if name.lower() in aliases:
        return UTF8Codec()


class Latin1Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.latin_1_encode(input, errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.latin_1_decode(input, errors)


def ibm_latin1(name):
    aliases = ['ibm1252', 'cp1252']
    if name.lower() in aliases:
        return Latin1Codec()


class Latin9Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso_8859_15', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso_8859_15', errors)


def ibm_latin9(name):
    aliases = ['ibm923', 'cp923', 'ibm924', 'cp924']
    if name.lower() in aliases:
        return Latin9Codec()


class IBM37Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp037', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp037', errors)


def ibm_37(name):
    aliases = ['ibm37', 'cp37']
    if name.lower() in aliases:
        return IBM37Codec()


class IBM813Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_7', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_7', errors)


def ibm_813(name):
    aliases = ['ibm813', 'cp813']
    if name.lower() in aliases:
        return IBM813Codec()


class IBM859Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_15', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_15', errors)


def ibm_859(name):
    aliases = ['ibm859', 'cp859']
    if name.lower() in aliases:
        return IBM859Codec()


class IBM867Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp862', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp862', errors)


def ibm_867(name):
    aliases = ['ibm867', 'cp867']
    if name.lower() in aliases:
        return IBM867Codec()


class IBM874Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp838', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp838', errors)


def ibm_874(name):
    aliases = ['ibm874', 'cp874']
    if name.lower() in aliases:
        return IBM874Codec()


class IBM912Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_2', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_2', errors)


def ibm_912(name):
    aliases = ['ibm912', 'cp912']
    if name.lower() in aliases:
        return IBM912Codec()


class IBM915Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_5', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_5', errors)


def ibm_915(name):
    aliases = ['ibm915', 'cp915']
    if name.lower() in aliases:
        return IBM915Codec()


class IBM916Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_8', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_8', errors)


def ibm_916(name):
    aliases = ['ibm916', 'cp916']
    if name.lower() in aliases:
        return IBM916Codec()


class IBM920Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_9', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_9', errors)


def ibm_920(name):
    aliases = ['ibm920', 'cp920']
    if name.lower() in aliases:
        return IBM920Codec()


class IBM921Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ascii', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ascii', errors)


def ibm_921(name):
    aliases = ['ibm921', 'cp921']
    if name.lower() in aliases:
        return IBM921Codec()


class IBM922Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ascii', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ascii', errors)


def ibm_922(name):
    aliases = ['ibm922', 'cp922']
    if name.lower() in aliases:
        return IBM922Codec()


class IBM923Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_15', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_15', errors)


def ibm_923(name):
    aliases = ['ibm923', 'cp923']
    if name.lower() in aliases:
        return IBM923Codec()


class IBM924Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_15', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_15', errors)


def ibm_924(name):
    aliases = ['ibm924', 'cp924']
    if name.lower() in aliases:
        return IBM924Codec()


class IBM942Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ascii', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ascii', errors)


def ibm_942(name):
    aliases = ['ibm942', 'cp942']
    if name.lower() in aliases:
        return IBM942Codec()


class IBM943Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ms932', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ms932', errors)


def ibm_943(name):
    aliases = ['ibm943', 'cp943']
    if name.lower() in aliases:
        return IBM943Codec()


class IBM948Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ms932', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ms932', errors)


def ibm_948(name):
    aliases = ['ibm948', 'cp948']
    if name.lower() in aliases:
        return IBM948Codec()


class IBM949Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ascii', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ascii', errors)


def ibm_949(name):
    aliases = ['ibm949', 'cp949']
    if name.lower() in aliases:
        return IBM949Codec()


class IBM954Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'euc_jp', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'euc_jp', errors)


def ibm_954(name):
    aliases = ['ibm954', 'cp954']
    if name.lower() in aliases:
        return IBM954Codec()


class IBM964Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ascii', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ascii', errors)


def ibm_964(name):
    aliases = ['ibm964', 'cp964']
    if name.lower() in aliases:
        return IBM964Codec()


class IBM970Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'euc_kr', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'euc_kr', errors)


def ibm_970(name):
    aliases = ['ibm970', 'cp970', 'ibm971', 'cp971']
    if name.lower() in aliases:
        return IBM970Codec()


class IBM1089Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso8859_6', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso8859_6', errors)


def ibm_1089(name):
    aliases = ['ibm1089', 'cp1089']
    if name.lower() in aliases:
        return IBM1089Codec()


class IBM1363Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'ms949', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'ms949', errors)


def ibm_1363(name):
    aliases = ['ibm1363', 'cp1363']
    if name.lower() in aliases:
        return IBM1363Codec()


class IBM1375Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'big5_hkscs', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'big5_hkscs', errors)


def ibm_1375(name):
    aliases = ['ibm1375', 'cp1375']
    if name.lower() in aliases:
        return IBM1375Codec()


class IBM1383Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'euc_cn', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'euc_cn', errors)


def ibm_1383(name):
    aliases = ['ibm1383', 'cp1383']
    if name.lower() in aliases:
        return IBM1383Codec()


class IBM1386Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'gbk', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'gbk', errors)


def ibm_1386(name):
    aliases = ['ibm1386', 'cp1386']
    if name.lower() in aliases:
        return IBM1386Codec()


class IBM1392Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'gb18030', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'gb18030', errors)


def ibm_1392(name):
    aliases = ['ibm1392', 'cp1392']
    if name.lower() in aliases:
        return IBM1392Codec()


class IBM5050Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'jisx0213', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'jisx0213', errors)


def ibm_5050(name):
    aliases = ['ibm5050', 'cp5050']
    if name.lower() in aliases:
        return IBM5050Codec()


class IBM5054Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso_2022_jp', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso_2022_jp', errors)


def ibm_5054(name):
    aliases = ['ibm5054', 'cp5054']
    if name.lower() in aliases:
        return IBM5054Codec()


class IBM5346Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1250', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1250', errors)


def ibm_5346(name):
    aliases = ['ibm5346', 'cp5346']
    if name.lower() in aliases:
        return IBM5346Codec()


class IBM5347Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1251', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1251', errors)


def ibm_5347(name):
    aliases = ['ibm5347', 'cp5347']
    if name.lower() in aliases:
        return IBM5347Codec()


class IBM5348Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1252', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1252', errors)


def ibm_5348(name):
    aliases = ['ibm5348', 'cp5348']
    if name.lower() in aliases:
        return IBM5348Codec()


class IBM5349Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1253', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1253', errors)


def ibm_5349(name):
    aliases = ['ibm5349', 'cp5349']
    if name.lower() in aliases:
        return IBM5349Codec()


class IBM5350Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1254', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1254', errors)


def ibm_5350(name):
    aliases = ['ibm5350', 'cp5350']
    if name.lower() in aliases:
        return IBM5350Codec()


class IBM5351Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1255', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1255', errors)


def ibm_5351(name):
    aliases = ['ibm5351', 'cp5351']
    if name.lower() in aliases:
        return IBM5351Codec()


class IBM5352Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1256', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1256', errors)


def ibm_5352(name):
    aliases = ['ibm5352', 'cp5352']
    if name.lower() in aliases:
        return IBM5352Codec()


class IBM5353Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1257', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1257', errors)


def ibm_5353(name):
    aliases = ['ibm5353', 'cp5353']
    if name.lower() in aliases:
        return IBM5353Codec()


class IBM5354Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp1258', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp1258', errors)


def ibm_5354(name):
    aliases = ['ibm5354', 'cp5354']
    if name.lower() in aliases:
        return IBM5354Codec()


class IBM5488Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'gb18030', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'gb18030', errors)


def ibm_5488(name):
    aliases = ['ibm5488', 'cp5488']
    if name.lower() in aliases:
        return IBM5488Codec()


class IBM9030Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'cp838', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'cp838', errors)


def ibm_9030(name):
    aliases = ['ibm9030', 'cp9030']
    if name.lower() in aliases:
        return IBM9030Codec()


class IBM25546Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'iso_2022_kr', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'iso_2022_kr', errors)


def ibm_25546(name):
    aliases = ['ibm25546', 'cp25546']
    if name.lower() in aliases:
        return IBM25546Codec()


class IBM33722Codec(codecs.Codec):
    def encode(self, input, errors='strict'):  # noqa
        return codecs.encode(input, 'euc_jp', errors)

    def decode(self, input, errors='strict'):  # noqa
        return codecs.decode(input, 'euc_jp', errors)


def ibm_33722(name):
    aliases = ['ibm33722', 'cp33722']
    if name.lower() in aliases:
        return IBM33722Codec()
