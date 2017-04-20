# -*- coding: utf-8 -*-
__author__ = 'PCPC'
import zlib
import codecs


def decode_gzip(data):
    decode_data = zlib.decompress(data, 16 | zlib.MAX_WBITS)


def encode_url_utf8(data):
    hex_data = codecs.encode(data, 'hex')
    ret = ''
    for i, v in enumerate(hex_data):
        if i % 2 == 0:
            ret += r'%'
        ret += v
    return ret
