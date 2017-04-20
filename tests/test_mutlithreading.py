# -*- coding: utf-8 -*-
__author__ = 'PCPC'
import threading


def A():
    with open('../server/conf/interface.json') as f:
        s = ''
        while s != 'Null':
            s = f.readline()
            print(s)


def B():
    with open('../server/func.py') as f:
        s = ''
        while s != 'Null':
            s = f.readline()
            print(s)


ta = threading.Thread(target=A)
tb = threading.Thread(target=B)
ta.start()
tb.start()
ta.join()
tb.join()
