# -*- coding: utf-8 -*-
__author__ = 'PCPC'
from server.autogen import *

j = r'''
{"reqeuestBody":[
            {
               "infoname": "IMEI",
                "value": "loc.map.baidu.com",
                "regex": "[^\"\\r\\n]+"
            }
        ],
        "responsebody": [
            {
                "infoname": "PositionDesc",
                "value": "content~addr~上海市,上海市,普陀区,共青路,,289,中国,0",
                "regex": "[^\"\\r\\n]+"
            },
            {
                "infoname": "PositionAcc",
                "value": "content~radius~67.625394",
                "regex": "[^\"\\r\\n]+"
            },
            {
                "infoname": "PositionLng",
                "value": "content~point~x~121.403368",
                "regex": "[^\"\\r\\n]+"
            },
            {
                "infoname": "PositionLat",
                "value": "content~point~y~31.228084",
                "regex": "[^\"\\r\\n]+"
            }
        ]
}
'''
print(parse_locations(j))
