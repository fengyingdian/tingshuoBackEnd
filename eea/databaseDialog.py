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
class databaseDialog:
    #
    def __init__(self, database):
        self.db = database

    def init(self):
        self.createDialogTable()
        self.createDialogContentTable()
        self.createDialogPunchTable()
        self.createDialogPunchContentTable()

    ########################################################################
    ########################################################################
    #dialog
    def createDialogTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS dialog (
                 title VARCHAR (100) not null,
                 name VARCHAR (100) not null,
                 time INT (100) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertDialog(self, title = str(), name = str(), time = int()):
        #Check if exists
        sql = "select * from dialog where title = '%s' and name = '%s' limit 1" % (title, name)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into dialog(title, name, time) values('%s', '%s', %d)" % (title, name, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getDialog(self, title = str(), name = str()):
        sql = "select * from dialog where title = '%s' and name = '%s' limit 1" % (title, name)
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
    def getDialogs(self):
        sql = "select * from dialog"
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
    #dialog content
    def createDialogContentTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS dialogContent (
                 courseId INT (20) not null,
                 role VARCHAR (100) not null,
                 content VARCHAR (512) not null,
                 translate VARCHAR (512) not null,
                 audioSrc VARCHAR (512) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertDialogContent(self, courseId = int(), role = str(), content = str(), translate = str(), audioSrc = str()):
        #Check if exists
        sql = "select * from dialogContent where courseId = %d and role = '%s' and content = '%s' limit 1" % (courseId, role, content)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into dialogContent(courseId, role, content, translate, audioSrc) values(%d, '%s', '%s', '%s', '%s')" % (courseId, role, content, translate, audioSrc)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getDialogContentByCourseId(self, courseId = int()):
        sql = "select * from dialogContent where courseId = %d" % courseId
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
    def getDialogContent(self, courseId = int(), role = str()):
        sql = "select * from dialogContent where courseId = %d and role = '%s'" % (courseId, role)
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
    # dialog punch
    def createDialogPunchTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS dialogPunch (
                 courseId INT (20) not null,
                 usrId INT (20) not null,
                 time INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertDialogPunch(self, courseId=int(), usrId=int(), time=int()):
        # Check if exists
        sql = "select * from dialogPunch where courseId = %d and usrId = %d and time = %d limit 1" % (courseId, usrId, time)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into dialogPunch(courseId, usrId, time) values(%d, %d, %d)" % (courseId, usrId, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getDialogPunch1(self, courseId=int(), usrId=int(), time=int()):
        sql = "select * from dialogPunch where courseId = %d and usrId = %d and time = %d limit 1" % (courseId, usrId, time)
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
    def getDialogPunch2(self, courseId=int(), usrId=int()):
        sql = "select * from dialogPunch where courseId = %d and usrId = %d" % (courseId, usrId)
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
    def getDialogPunchByCourseId(self, courseId=int()):
        sql = "select * from dialogPunch where courseId = %d" % courseId
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
    def getDialogPunchByUsrId(self, usrId=int()):
        sql = "select * from dialogPunch where usrId = %d" % usrId
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
    # dialog punch content
    def createDialogPunchContentTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS dialogPunchContent (
                 punchId INT (20) not null,
                 contentId INT (20) not null,
                 id INT(20) AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertDialogPunchContent(self, punchId=int(), contentId=int()):
        # Check if exists
        sql = "select * from dialogPunchContent where punchId = %d and contentId = %d limit 1" % (punchId, contentId)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into dialogPunchContent(punchId, contentId) values(%d, %d)" % (punchId, contentId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getDialogPunchContentByPunchId(self, punchId):
        sql = "select * from dialogPunchContent where punchId = %d" % punchId
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
    def getDialogPunchContentById(self, id):
        sql = "select * from dialogPunchContent where id = %d limit 1" % id
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []
