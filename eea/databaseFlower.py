#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import os
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

import database as db
import time
import types
import os

#
class databaseFlower:
    #
    def __init__(self, database):
        self.db = database

    def init(self):
        self.createFlowerTable()
        self.createFlowerEventTable()
        self.createCommentBookEventTable()

    ########################################################################
    ########################################################################
    #flower
    def createFlowerTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS flower (
                 usrId INT (20) not null,
                 sum INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertFlower(self, usrId = int(), sum = int()):
        sql = "insert into flower(usrId, sum) values(%d, %d)" % (usrId, sum)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def modifyFlower(self, usrId = int(), count = int()):
        # Check if exists
        sql = "select * from flower where usrId = %d limit 1" % usrId
        if self.db.execute(sql) == 0:
            return self.insertFlower(usrId,count), count
        row = self.db.cur.fetchone()
        sum = row[1] + count
        sql = "update flower set sum = %d where usrId = %d" % (sum, usrId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success", sum

    #
    def getFlower(self, usrId = int()):
        sql = "select * from flower where usrId = %d limit 1" % usrId
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    ########################################################################
    ########################################################################
    #flower event
    def createFlowerEventTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS flowerEvent (
                 usrId INT (20) not null,
                 toUsrId INT (20) not null,
                 eventCode INT (20) not null,   
                 count INT (20) not null,
                 time INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)
        #[eventCode]-[event]([count]): 10000-充值(n)，10001-打卡(5)，10002-语音点评(3)，10003-文字点评(2)，10004-点赞(1)，10005-被打赏(n)
        #[eventCode]-[event]([count]): 20001-删除打卡(-5)，20002-删除语音点评(-3)，10003-删除文字点评(-2)，10004-取消点赞(-1)，20005-打赏(n)

    #
    def insertFlowerEvent(self, usrId = int(), toUsrId = int(), eventCode = int(), count = int(), time = int()):
        # Check if exists
        sql = "select * from flowerEvent where usrId = %d and toUsrId = %d and eventCode = %d and time = %d" % (usrId, toUsrId, eventCode, time)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into flowerEvent(usrId, toUsrId, eventCode, count, time) values(%d, %d, %d, %d, %d)" % (usrId, toUsrId, eventCode, count, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getFlowerEventById(self, id = int()):
        sql = "select * from flowerEvent where id = %d limit 1" % id
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    #
    def getFlowerEventByUsrId(self, usrId = int()):
        sql = "select * from flowerEvent where usrId = %d" % usrId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    #
    def getFlowerEvent(self, usrId = int(), toUsrId = int(), eventCode = int(), time = int()):
        # Check if exists
        sql = "select * from flowerEvent where usrId = %d and toUsrId = %d and eventCode = %d and time = %d limit 1" % (usrId, toUsrId, eventCode, time)
        if self.db.execute(sql) != 0:
            return self.db.cur.fetchone()
        else:
            return []

    ########################################################################
    ########################################################################
    #comment book event
    def createCommentBookEventTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS commentBookEvent(
                 usrId INT (20) not null,
                 toUsrId INT (20) not null,
                 punchId INT (20) not null,
                 eventCode INT (20) not null,
                 count INT (20) not null,
                 time1 INT (20) not null,
                 time2 INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)
        #[eventCode]-[event]: 30000-预约等待中，30001-已点评，30002-被拒绝，30003-已超时，30004-已取消(目前不开放)

    #
    def insertCommentBookEvent(self, usrId = int(), toUsrId = int(), punchId = int(), eventCode = int(), count = int(), time = int()):
        # Check if exists
        sql = "select * from commentBookEvent where usrId = %d and toUsrId = %d and punchId = %d and eventCode = %d" % (usrId, toUsrId, punchId, eventCode)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into commentBookEvent(usrId, toUsrId, punchId, eventCode, count, time1, time2) values(%d, %d, %d, %d, %d, %d, %d)" % (usrId, toUsrId, punchId, eventCode, count, time, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def modifyCommentBookEvent(self, usrId = int(), toUsrId = int(), punchId = int(), eventCode = int(), time = int()):
        # Check if exists
        sql = "select * from commentBookEvent where usrId = %d and toUsrId = %d and punchId = %d and eventCode = 30000" % (usrId, toUsrId, punchId)
        if self.db.execute(sql) == 0:
            return "not existed"

        sql = "update commentBookEvent set eventCode = %d, time2 = %d where usrId = %d and toUsrId = %d and punchId = %d and eventCode = 30000" % (eventCode, time, usrId, toUsrId, punchId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getCommentBookEventById(self, id = int()):
        sql = "select * from commentBookEvent where id = %d limit 1" % id
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    #
    def getCommentBookEventByUsrId(self, usrId = int()):
        sql = "select * from commentBookEvent where usrId = %d" % usrId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    #
    def getCommentBookEventByToUsrId(self, toUsrId = int()):
        sql = "select * from commentBookEvent where toUsrId = %d" % toUsrId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    #
    def getCommentBookEvent(self, usrId = int(), toUsrId = int(), punchId = int(), eventCode = int(), time = int()):
        # Check if exists
        sql = "select * from commentBookEvent where usrId = %d and toUsrId = %d and punchId = %d and eventCode = %d and time = %d limit 1" % (usrId, toUsrId, punchId, eventCode, time)
        if self.db.execute(sql) != 0:
            return self.db.cur.fetchone()
        else:
            return []