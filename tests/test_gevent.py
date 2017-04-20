# -*- coding: utf-8 -*-
__author__ = 'PCPC'
from gevent import monkey;

monkey.patch_all()


def A():
    with open('../server/conf/interface.json') as f:
        print(f.read())


def B():
    with open('../server/func.py') as f:
        print(f.read())


import gevent

gevent.joinall([gevent.spawn(A),
                gevent.spawn(B)])
