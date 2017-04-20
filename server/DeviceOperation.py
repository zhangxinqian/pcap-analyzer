#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net
from server import *
import unittest
import sqlite3
import func
__author__ = 'hx'
class DeviceInfo:
    def __init__(self):
        self.db=func.connect_db()
    def closeDB(self):
        self.db.commit()
        self.db.close()
    def addDeviceInfo(self,device_id='',device_name='',device_imei='',device_os='',device_SerialNumber=''):
        self.db.cursor().execute("insert into deviceInfo(device_id,device_name,device_imei,device_os,device_SerialNumber)  values(?,?,?,?,?)",(device_id,device_name,device_imei,device_os,device_SerialNumber))
        DeviceInfo.closeDB(self)
    def deleteDeviceInfo(self,device_no):
        self.db.execute("delete from deviceInfo where device_no=?",device_no)
        DeviceInfo.closeDB(self)
    def getDeviceInfo(self):
        cursor=self.db.execute("select * from deviceInfo deviceInfo")
        entries = [dict(device_no=row[0], device_id=row[1], device_name=row[2], device_imei=row[3],device_os=row[4],device_SerialNumber=row[5]) for row in cursor.fetchall()]
        DeviceInfo.closeDB(self)
        return entries

# 获取数据库连接

