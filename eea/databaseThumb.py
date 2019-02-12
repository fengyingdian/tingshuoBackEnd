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
class databaseThumb:
    #
    def __init__(self, database):
        self.db = database

    def init(self):
        self.createPunchThumbTable()
        self.createCommentThumbTable()

    ########################################################################
    ########################################################################
    #punchThumb
    def createPunchThumbTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS punchThumb (
                 punchId INT (20) not null,
                 usrId INT (20) not null,
                 time INT (20) not null,
                 status INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertPunchThumb(self, punchId = int(), usrId = int(), time = int()):
        #Check if exists
        sql = "select * from punchThumb where punchId = %d and usrId = %d limit 1" % (punchId, usrId)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into punchThumb(punchId, usrId, time, status) values(%d, %d, %d, 1)" % (punchId, usrId, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def modifyPunchThumb(self, punchId = int(), usrId = int(), time = int(), status = int()):
        # Check if exists
        sql = "select * from punchThumb where punchId = %d and usrId = %d limit 1" % (punchId, usrId)
        if self.db.execute(sql) == 0:
            self.insertPunchThumb(punchId,usrId,time)
            return "success"

        sql = "update punchThumb set status = %d where punchId = %d and usrId = %d limit 1" % (status, punchId, usrId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getPunchThumb(self, punchId = int(), usrId = int()):
        sql = "select * from punchThumb where punchId = %d and usrId = %d limit 1" % (punchId, usrId)
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return None
        else:
            return None

    #
    def getPunchThumbs(self, punchId = int()):
        sql = "select * from punchThumb where punchId = %d and status = 1" % punchId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []

    ########################################################################
    ########################################################################
    #commentThumb
    def createCommentThumbTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS commentThumb (
                 commentId INT (20) not null,
                 usrId INT (20) not null,
                 time INT (20) not null,
                 status INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertCommentThumb(self, commentId = int(), usrId = int(), time = int()):
        #Check if exists
        sql = "select * from commentThumb where commentId = %d and usrId = %d limit 1" % (commentId, usrId)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into commentThumb(commentId, usrId, time, status) values(%d, %d, %d, 1)" % (commentId, usrId, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def modifyCommentThumb(self, commentId = int(), usrId = int(), time = int(), status = int()):
        # Check if exists
        sql = "select * from commentThumb where commentId = %d and usrId = %d limit 1" % (commentId, usrId)
        if self.db.execute(sql) == 0:
            self.insertCommentThumb(commentId,usrId,time)
            return "success"

        sql = "update commentThumb set status = %d where commentId = %d and usrId = %d limit 1" % (status, commentId, usrId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getCommentThumb(self, commentId = int(), usrId = int()):
        sql = "select * from commentThumb where commentId = %d and usrId = %d limit 1" % (commentId, usrId)
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return None
        else:
            return None

    #
    def getCommentThumbs(self, commentId = int()):
        sql = "select * from commentThumb where commentId = %d and status = 1" % commentId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []
