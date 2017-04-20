#!/usr/bin/env python
# -*- coding: utf-8 -*-
# author: le4f.net
from server import *
import unittest
import sqlite3
import func
__author__ = 'hx'
class userInfo:
    def __init__(self):
        self.db=func.connect_db()
    def closeDB(self):
        self.db.commit()
        self.db.close()
    def addUserInfo(self,user_id='',user_name='',user_companyName='',
                    user_Title='',user_mobile='',user_email='',user_groupName='',user_address='',user_nickname='',
                    user_birthday='',user_notes=''):
        self.db.cursor().execute("insert into userInfo(user_name,user_companyName,user_Title,user_mobile,user_email,user_groupName,user_address,user_nickname,user_birthday,user_notes)  values(?,?,?,?,?,?,?,?,?,?)",
                                 (user_name,user_companyName,user_Title,user_mobile,user_email,user_groupName,user_address,user_nickname,user_birthday,user_notes))
        userInfo.closeDB(self)
    def deleteUserInfo(self,user_id):
        self.db.execute("delete from userInfo where user_id=?",user_id)
        userInfo.closeDB(self)
    def getUserInfo(self):
        cursor=self.db.execute('select * from userInfo')
        entries = [dict(user_id=row[0], user_name=row[1], user_companyName=row[2],
                        user_Title=row[3],user_mobile=row[4],user_email=row[5],
                        user_groupName=row[6],user_address=row[7],user_nickname=row[8],
                    user_birthday=row[9],user_notes=row[10]) for row in cursor.fetchall()]
        userInfo.closeDB(self)
        return entries
