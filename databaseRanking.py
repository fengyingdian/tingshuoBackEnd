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
class databaseRanking:
    #
    def __init__(self, database):
        self.db = database
        self.createPunchRankingTable()
        self.createCommentRankingTable()

    ########################################################################
    ########################################################################
    #punchRanking
    def createPunchRankingTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS punchRanking (
                 date VARCHAR (100) not null,
                 usrId INT (20) not null,
                 punchTime INT (20) not null,
                 commentTime INT (20) not null,
                 rank INT (20) not null,
                 time INT (20) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertPunchRanking(self, date = str(), usrId = int(), punchTime = int(), commentTime = int(), rank = int(), time = int()):
        #Check if exists
        sql = "select * from punchRanking where date = '%s' and usrId = %d limit 1" % (date, usrId)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into punchRanking(date, usrId, punchTime, commentTime, rank, time) values('%s', %d, %d, %d, %d, %d)" % (date, usrId, punchTime, commentTime, rank, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getPunchRanking(self, date = str()):
        sql = "select * from punchRanking where date = '%s' limit 50" %date
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
    #commentRanking
    def createCommentRankingTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS commentRanking (
                 date VARCHAR (100) not null,
                 usrId INT (20) not null,
                 commentTime INT (20) not null,
                 rank INT (20) not null,
                 time INT (20) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertCommentRanking(self, date = str(), usrId = int(), commentTime = int(), rank = int(), time = int()):
        #Check if exists
        sql = "select * from commentRanking where date = '%s' and usrId = %d limit 1" % (date, usrId)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into commentRanking(date, usrId, commentTime, rank, time) values('%s', %d, %d, %d, %d)" % (date, usrId, commentTime, rank, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getcommentRanking(self, date = str()):
        sql = "select * from commentRanking where date = '%s' limit 50" % date
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() > 0:
                return row
            else:
                return []
        else:
            return []