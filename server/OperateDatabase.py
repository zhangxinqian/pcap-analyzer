#!/usr/bin/env python
# -*- coding: utf-8 -*-

from server import *


# 连接数据库
def connect_db():
    return sqlite3.connect('db/db.sqlite')


def addDeviceInfo(device_id, device_name, device_imei, device_os, device_SerialNumber):
    db = connect_db()
    # print("test")
    db.cursor().execute(
        "INSERT INTO deviceInfo(device_id,device_name,device_imei,device_os,device_SerialNumber)  VALUES(?,?,?,?,?)",
        (device_id, device_name, device_imei, device_os, device_SerialNumber))
    db.commit()
    db.close()


def CreateDeviceInfo():
    db = connect_db()
    db.execute("DROP TABLE deviceInfo")
    db.execute("CREATE TABLE deviceInfo("
               "device_no INTEGER PRIMARY KEY AUTOINCREMENT,"
               "device_id    NVARCHAR(50) NOT NULL, "
               "device_name NVARCHAR(50) NOT NULL,"
               "device_imei  NVARCHAR(20) NOT NULL,"
               "device_os NVARCHAR(20),"
               "device_SerialNumber NVARCHAR(20))")
    db.commit()
    db.close()


def UpdateDeviceInfo(device_no, device_id, device_name, device_imei, device_os, device_SerialNumber):
    db = connect_db()
    db.execute("UPDATE deviceInfo SET device_id=?,device_name=?,device_imei=?,device_os=?,device_SerialNumber=?"
               "WHERE device_no=?", device_id, device_name, device_imei, device_os, device_SerialNumber, device_no)
    db.commit()
    db.close()


def DeleteDeviceInfo(device_no):
    db = connect_db()
    db.execute("DELETE FROM deviceInfo WHERE device_no=?", device_no)


def GetDeviceCount(device_id='', device_name='', device_imei='', device_SerialNumber='', device_os=''):
    db = connect_db()
    count = db.execute("SELECT count(*) FROM deviceInfo "
                       "WHERE (device_id=? OR ? IS NULL) AND "
                       "(device_name=? OR ? IS NULL)"
                       " AND (device_imei=? OR ? IS NULL) AND"
                       " (device_SerialNumber=? OR ? IS NULL) AND "
                       "(device_os=? OR ? IS NULL)",
                       (device_id, device_id, device_name, device_name, device_imei, device_imei, device_SerialNumber,
                        device_SerialNumber, device_os, device_os))
    # count=db.execute("select count(*) from deviceInfo")
    return count.fetchall()


def ShowDeviceInfo(pageNum, device_id='', device_name='', device_imei='', device_SerialNumber='',
                   device_os=''):  # 是否需要排序问题，以及分页
    db = connect_db()
    pageCount = 10
    count = GetDeviceCount(device_id, device_name, device_imei, device_SerialNumber, device_os)
    # pageNum不能超过当前最大页数
    '''cursor=db.execute("select rowid as num,d.* from deviceInfo d where "
                      " (d.device_id=? or ? isnull) and (d.device_name=? or ? isnull) and(d.device_imei=? or ? isnull)"
                      " and (d.device_SerialNumber=? or ? isnull) and (d.device_os=? or ? isnull)"
                      " order by num limit (?-1)*?,?*?",(device_id,device_id,device_name,device_name,device_imei,device_imei,
                                                         device_SerialNumber,device_SerialNumber,
                                                         device_os,device_os,pageNum,pageCount,pageNum,pageCount))
    '''
    # 拼接SQL
    sql = 'select rowid as num,d.* from (select * from deviceInfo dd where 1=1 '
    if device_id.strip():
        sql += " and dd.device_id='" + device_id + "'"
    if device_name.strip():
        sql += " and dd.device_name='" + device_name + "'"
    if device_imei.strip():
        sql += " and dd.device_imei='" + device_imei + "'"
    if device_SerialNumber.strip():
        sql += " and dd.device_SerialNumber='" + device_SerialNumber + "'"
    if device_os.strip():
        sql += " and dd.device_os='" + device_os + "'"
    sql += ')d order by num limit (?-1)*?,?*?'
    print sql
    # cursor=db.execute("select rowid as num,d.* from (select * from deviceInfo dd where (? IS NULL or dd.device_os=?)) d"
    #
    #                  " order by num limit (?-1)*?,?*?",(device_os,device_os,pageNum,pageCount,pageNum,pageCount))
    # cursor=db.execute(sql,(device_id,device_name,device_imei,device_SerialNumber,device_os,pageNum,pageCount,pageNum,pageCount))
    cursor = db.execute(sql, (pageNum, pageCount, pageNum, pageCount))
    print cursor.fetchone()
    entries = [dict(device_no=row[1], device_id=row[2], device_name=row[3], device_imei=row[4], device_os=row[5],
                    device_SerialNumber=row[6]) for row in cursor.fetchall()]
    db.commit()
    db.close()
    return entries

    # cursor=db.execute("select * from deviceInfo");
    # for row in cursor.fetchall():
    #    print row


if __name__ == '__main__':
    print("hello world");
    # CreateDeviceInfo() #创建表
    # 添加数据
    # CreateDeviceInfo()
    # addDeviceInfo ('0000000001','xiaomi00001','000000000000001','xiaomi','00000000000000000001')
    '''for i in range(1,100):
        strs=''
        if i<10:
            strs='0'+str(i)
        else:
            strs=str(i)
        addDeviceInfo ('0000000001','xiaomi00001','000000000000001','123456','00000000000000000001')
'''
    ShowDeviceInfo(1, '', '', '', '', '')
