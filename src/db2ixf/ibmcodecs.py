# coding=utf-8
"""Add new aliases that maps ibm code pages to python encodings."""
import codecs
import ebcdic


def add_encoding_alias(old_name, new_name):
    old = codecs.lookup(old_name)
    new = codecs.CodecInfo(
        old.encode, old.decode,
        streamreader=old.streamreader,
        streamwriter=old.streamwriter,
        incrementalencoder=old.incrementalencoder,
        incrementaldecoder=old.incrementaldecoder,
        name=new_name
    )
    return new


def ibm_utf_32_be(name):
    aliases = ['ibm1232', 'cp1232', 'ibm1233', 'cp1233']
    if name.lower() in aliases:
        return add_encoding_alias('utf_32_be', name)


def ibm_utf_32_le(name):
    aliases = ['ibm1234', 'cp1234', 'ibm1235', 'cp1235']
    if name.lower() in aliases:
        return add_encoding_alias('utf_32_le', name)


def ibm_utf_32(name):
    aliases = ['ibm1236', 'cp1236', 'ibm1237', 'cp1237']
    if name.lower() in aliases:
        return add_encoding_alias('utf_32', name)


def ibm_utf_16_be(name):
    aliases = ['ibm1200', 'cp1200', 'ibm1201', 'cp1201']
    if name.lower() in aliases:
        return add_encoding_alias('utf_16_be', name)


def ibm_utf_16_le(name):
    aliases = ['ibm1202', 'cp1202', 'ibm1203', 'cp1203']
    if name.lower() in aliases:
        return add_encoding_alias('utf_16_le', name)


def ibm_utf_16(name):
    aliases = ['ibm1204', 'cp1204', 'ibm1205', 'cp1205']
    if name.lower() in aliases:
        return add_encoding_alias('utf_16', name)


def ibm_utf_8(name):
    aliases = ['ibm1208', 'cp1208', 'ibm1209', 'cp1209']
    if name.lower() in aliases:
        return add_encoding_alias('utf_8', name)


def ibm_latin1(name):
    aliases = ['ibm1252']
    if name.lower() in aliases:
        return add_encoding_alias('latin_1', name)


def ibm_latin9(name):
    aliases = ['ibm923', 'cp923', 'ibm924', 'cp924']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_15', name)


def ibm_37(name):
    aliases = ['ibm37', 'cp37']
    if name.lower() in aliases:
        return add_encoding_alias('cp037', name)


def ibm_39(name):
    aliases = ['ibm39', 'cp39']
    if name.lower() in aliases:
        return add_encoding_alias('cp037', name)


def ibm_813(name):
    aliases = ['ibm813', 'cp813']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_7', name)


def ibm_859(name):
    aliases = ['ibm859', 'cp859']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_15', name)


def ibm_867(name):
    aliases = ['ibm867', 'cp867']
    if name.lower() in aliases:
        return add_encoding_alias('cp862', name)


def ibm_874(name):
    aliases = ['ibm874', 'cp874']
    if name.lower() in aliases:
        return add_encoding_alias('cp838', name)


def ibm_912(name):
    aliases = ['ibm912', 'cp912']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_2', name)


def ibm_915(name):
    aliases = ['ibm915', 'cp915']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_5', name)


def ibm_916(name):
    aliases = ['ibm916', 'cp916']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_8', name)


def ibm_920(name):
    aliases = ['ibm920', 'cp920']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_9', name)


def ibm_921(name):
    aliases = ['ibm921', 'cp921']
    if name.lower() in aliases:
        return add_encoding_alias('ascii', name)


def ibm_922(name):
    aliases = ['ibm922', 'cp922']
    if name.lower() in aliases:
        return add_encoding_alias('ascii', name)


def ibm_923(name):
    aliases = ['ibm923', 'cp923']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_15', name)


def ibm_924(name):
    aliases = ['ibm924', 'cp924']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_15', name)


def ibm_943(name):
    aliases = ['ibm943', 'cp943']
    if name.lower() in aliases:
        return add_encoding_alias('shift_jis', name)


def ibm_947(name):
    aliases = ['ibm947', 'cp947']
    if name.lower() in aliases:
        return add_encoding_alias('big5', name)


def ibm_951(name):
    aliases = ['ibm951', 'cp951']
    if name.lower() in aliases:
        return add_encoding_alias('cp949', name)


def ibm_954(name):
    aliases = ['ibm954', 'cp954']
    if name.lower() in aliases:
        return add_encoding_alias('euc_jp', name)


def ibm_964(name):
    aliases = ['ibm964', 'cp964']
    if name.lower() in aliases:
        return add_encoding_alias('ascii', name)


def ibm_970(name):
    aliases = ['ibm970', 'cp970', 'ibm971', 'cp971']
    if name.lower() in aliases:
        return add_encoding_alias('euc_kr', name)


def ibm_1088(name):
    aliases = ['ibm1088', 'cp1088']
    if name.lower() in aliases:
        return add_encoding_alias('euc_kr', name)


def ibm_1089(name):
    aliases = ['ibm1089', 'cp1089']
    if name.lower() in aliases:
        return add_encoding_alias('iso8859_6', name)


def ibm_1098(name):
    aliases = ['ibm1097', 'cp1097']
    if name.lower() in aliases:
        return add_encoding_alias('cp1097', name)


def ibm_1114(name):
    aliases = ['ibm1114', 'cp1114']
    if name.lower() in aliases:
        return add_encoding_alias('big5', name)


def ibm_1115(name):
    aliases = ['ibm1115', 'cp1115']
    if name.lower() in aliases:
        return add_encoding_alias('gb2312', name)


def ibm_1124(name):
    aliases = ['ibm1124', 'cp1124']
    if name.lower() in aliases:
        return add_encoding_alias('cp1025', name)


def ibm_1351(name):
    aliases = ['ibm1351', 'cp1351']
    if name.lower() in aliases:
        return add_encoding_alias('iso2022_jp_ext', name)


def ibm_1362(name):
    aliases = ['ibm1362', 'cp1362']
    if name.lower() in aliases:
        return add_encoding_alias('iso2022_kr', name)


def ibm_1363(name):
    aliases = ['ibm1363', 'cp1363']
    if name.lower() in aliases:
        return add_encoding_alias('ms949', name)


def ibm_1375(name):
    aliases = ['ibm1375', 'cp1375']
    if name.lower() in aliases:
        return add_encoding_alias('big5_hkscs', name)


def ibm_1380(name):
    aliases = ['ibm1380', 'cp1380']
    if name.lower() in aliases:
        return add_encoding_alias('gb2312', name)


def ibm_1381(name):
    aliases = ['ibm1381', 'cp1381']
    if name.lower() in aliases:
        return add_encoding_alias('gb2312', name)


def ibm_1383(name):
    aliases = ['ibm1383', 'cp1383']
    if name.lower() in aliases:
        return add_encoding_alias('gb2312', name)


def ibm_1385(name):
    aliases = ['ibm1385', 'cp1385']
    if name.lower() in aliases:
        return add_encoding_alias('gbk', name)


def ibm_1386(name):
    aliases = ['ibm1386', 'cp1386']
    if name.lower() in aliases:
        return add_encoding_alias('gbk', name)


def ibm_1390(name):
    aliases = ['ibm1390', 'cp1390']
    if name.lower() in aliases:
        return add_encoding_alias('euc_jp', name)


def ibm_1392(name):
    aliases = ['ibm1392', 'cp1392']
    if name.lower() in aliases:
        return add_encoding_alias('gb18030', name)


def ibm_5050(name):
    aliases = ['ibm5050', 'cp5050']
    if name.lower() in aliases:
        return add_encoding_alias('euc_jis_2004', name)


def ibm_5054(name):
    aliases = ['ibm5054', 'cp5054']
    if name.lower() in aliases:
        return add_encoding_alias('iso_2022_jp', name)


def ibm_5346(name):
    aliases = ['ibm5346', 'cp5346']
    if name.lower() in aliases:
        return add_encoding_alias('cp1250', name)


def ibm_5347(name):
    aliases = ['ibm5347', 'cp5347']
    if name.lower() in aliases:
        return add_encoding_alias('cp1251', name)


def ibm_5348(name):
    aliases = ['ibm5348', 'cp5348']
    if name.lower() in aliases:
        return add_encoding_alias('cp1252', name)


def ibm_5349(name):
    aliases = ['ibm5349', 'cp5349']
    if name.lower() in aliases:
        return add_encoding_alias('cp1253', name)


def ibm_5350(name):
    aliases = ['ibm5350', 'cp5350']
    if name.lower() in aliases:
        return add_encoding_alias('cp1254', name)


def ibm_5351(name):
    aliases = ['ibm5351', 'cp5351']
    if name.lower() in aliases:
        return add_encoding_alias('cp1255', name)


def ibm_5352(name):
    aliases = ['ibm5352', 'cp5352']
    if name.lower() in aliases:
        return add_encoding_alias('cp1256', name)


def ibm_5353(name):
    aliases = ['ibm5353', 'cp5353']
    if name.lower() in aliases:
        return add_encoding_alias('cp1257', name)


def ibm_5354(name):
    aliases = ['ibm5354', 'cp5354']
    if name.lower() in aliases:
        return add_encoding_alias('cp1258', name)


def ibm_5488(name):
    aliases = ['ibm5488', 'cp5488']
    if name.lower() in aliases:
        return add_encoding_alias('gb18030', name)


def ibm_9030(name):
    aliases = ['ibm9030', 'cp9030']
    if name.lower() in aliases:
        return add_encoding_alias('cp838', name)


def ibm_9066(name):
    aliases = ['ibm9066', 'cp9066']
    if name.lower() in aliases:
        return add_encoding_alias('cp838', name)


def ibm_25546(name):
    aliases = ['ibm25546', 'cp25546']
    if name.lower() in aliases:
        return add_encoding_alias('iso_2022_kr', name)


def ibm_33722(name):
    aliases = ['ibm33722', 'cp33722']
    if name.lower() in aliases:
        return add_encoding_alias('euc_jp', name)


search_functions = (
    ebcdic._find_ebcdic_codec,  # noqa
    ibm_utf_32_be,
    ibm_utf_32_le,
    ibm_utf_32,
    ibm_utf_16_be,
    ibm_utf_16_le,
    ibm_utf_16,
    ibm_utf_8,
    ibm_latin1,
    ibm_latin9,
    ibm_37,
    ibm_39,
    ibm_813,
    ibm_859,
    ibm_867,
    ibm_874,
    ibm_912,
    ibm_915,
    ibm_916,
    ibm_920,
    ibm_921,
    ibm_922,
    ibm_923,
    ibm_924,
    ibm_943,
    ibm_947,
    ibm_951,
    ibm_954,
    ibm_964,
    ibm_970,
    ibm_1088,
    ibm_1089,
    ibm_1098,
    ibm_1114,
    ibm_1115,
    ibm_1124,
    ibm_1351,
    ibm_1362,
    ibm_1363,
    ibm_1375,
    ibm_1380,
    ibm_1381,
    ibm_1383,
    ibm_1385,
    ibm_1386,
    ibm_1390,
    ibm_1392,
    ibm_5050,
    ibm_5054,
    ibm_5346,
    ibm_5347,
    ibm_5348,
    ibm_5349,
    ibm_5350,
    ibm_5351,
    ibm_5352,
    ibm_5353,
    ibm_5354,
    ibm_5488,
    ibm_9030,
    ibm_9066,
    ibm_25546,
    ibm_33722,
)

__all__ = ["search_functions"]
