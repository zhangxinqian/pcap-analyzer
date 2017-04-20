# -*- coding: utf-8 -*-
__author__ = 'PCPC'


import simplejson as json

def as_complex(dct):
    if '__complex__' in dct:
        return complex(dct['real'], dct['imag'])
    return dct


# j = json.loads('{"__complex__": true, "real": 1, "imag": 2}', object_hook=as_complex)
# print(j)

j = json.loads(
    '{"content":{"addr":"上海市,上海市,普陀区,共青路,,289,中国,0","bldg":"","clf":"121.403753|31.227739|2000.000000","floor":"","indoor":"40","point":{"x":"121.403368","y":"31.228084"},"radius":"67.625394","ssid":"2047"},"result":{"error":"161","time":"2015-05-08 10:51:01"}}')
print(j)
