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
class databaseTable:
    #
    def __init__(self, database):
        self.db = database

    def init(self):
        self.createFormIdTable()
        self.createClassTable()
        self.createUsrClassTable()
        self.createUsrGradeTable()
        self.createClassCourseTable()

    ########################################################################
    ########################################################################
    #formId
    def createFormIdTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS formId (
                 openId VARCHAR (100) not null,
                 formId VARCHAR (100) not null,
                 time INT (20) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertFormId(self, openId = str(), formId = str()):
        #Check if exists
        sql = "select * from formId where openId = '%s' and formId = '%s' limit 1" % (openId, formId)
        if self.db.execute(sql) != 0:
            print ("existed")
            return "existed"

        insertTime = int(time.time())
        sql = "insert into formId(openId, formId, time) values('%s','%s', %d)" % (openId, formId, insertTime)
        self.db.execute(sql)
        self.db.con.commit()
        print ("success")
        return "success"

    #
    def getValidFormId(self, openId = str()):
        thisTime = int(time.time()) - 3600 * 24 * 7
        sql = "select * from formId where openId = '%s' and time > %d limit 1" % (openId, thisTime)
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() > 0:
                sql = "delete from formId where id = %d" % row[3]
                self.db.execute(sql)
                self.db.con.commit()
                return row[1]
            else:
                return []
        else:
            return []
			
	#
    def deleteFormId(self):
        thisTime = int(time.time()) - 3600 * 24 * 7
        sql = "delete from formId where time < %d " % thisTime
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        self.db.con.commit()
        if type(row) != type(None):
            if row.__len__() >0 :
                return "1"
            else:
                return "2"
        else:
            return "3"


    ########################################################################
    ########################################################################
    #class
    def createClassTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS class (
                 name VARCHAR (100) not null,
                 sName VARCHAR (100) not null,
                 type INT (20) not null,
                 maxCount INT (20) not null,
                 info VARCHAR (100) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 coverSrc VARCHAR (512),
                 admittance INT (20) not null,
                 punchLimit INT (20) not null,
                 time VARCHAR (100) not null,
                 usrId INT (20) not null,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertClass(self, name = str(), sName = str(), type = int(), maxCount = int(), info = str(), coverSrc = str(), admittance = int(), punchLimit = int(), time = str(), usrId = int()):
        #Check if exists
        sql = "select * from class where name = '%s' and sName = '%s' and type = %d limit 1" % (name, sName, type)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into class(name, sName, type, maxCount, info, coverSrc, admittance, punchLimit, time, usrId) values('%s','%s', %d, %d,'%s','%s', %d, %d,'%s', %d)" % (name, sName, type, maxCount, info, coverSrc, admittance, punchLimit, time, usrId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def modifyClass(self, name = str(), sName = str(), type = int(), maxCount = int(), info = str(), coverSrc = str(), admittance = int(), punchLimit = int(), usrId = int(), classId = int()):
        sql = "select * from usrClass where usrId = %d and id = %d limit 1" % (usrId, classId)
        if self.db.execute(sql) == 0:
            return "can't find"

        sql = "update class set name='%s', sName='%s', type=%d, maxCount=%d, info='%s', coverSrc'%s', admittance=%d, punchLimit=%d where usrId=%d and id=%d" % (name, sName, type, maxCount, info, coverSrc, admittance, punchLimit, usrId, classId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getClasses(self):
        sql = "select * from class"
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
    def getClassBysName(self, sName = str(), classType = int()):
        print("getClass: ", sName)
        sql = "select * from class where sName = '%s' and type = %d limit 1" % (sName, classType)
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
    def getClass(self, name = str(), sName = str(), classType = int()):
        print("getClass: ", name, sName, classType)
        sql = "select * from class where name = '%s' and sName = '%s' and type = %d limit 1" % (name, sName, classType)
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
    def getClassById(self, id = int()):
        sql = "select * from class where id = %d limit 1" % id
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
    def deleteClassById(self, id = int()):
        sql = "select * from class where id = %d limit 1" % id
        if self.db.execute(sql) != 1:
            self.existed = "not existed"
            self.self_existed = self.existed
            return self.self_existed

        sql = "delete from class where id = %d" % id
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    ########################################################################
    ########################################################################
    # usrClass
    # level：9创建者，8管理员，点评老师7，点评班长6，点评班助5，...， 0普通成员
    # status：1正常，2申请排队中，3退出，0淘汰
    def createUsrClassTable(self):
        # 创建数据表SQL语句
        self.id_ = """CREATE TABLE if not EXISTS usrClass (
                 usrId INT (20) not null,
                 classId INT (20) not null,
                 number INT (20) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 level INT (20) not null,
                 status INT (20) not null,
                 primary key(id))"""
        sql = self.id_
        self.db.execute(sql)

    #
    def insertUsrClass(self, usrId=int(), classId=int(), number=int(), level=int(), status=int()):
        # Check if exists
        sql = "select * from usrClass where usrId = %d and classId = %d limit 1" % (usrId, classId)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into usrClass(usrId, classId, number, level, status) values(%d, %d, %d, %d, %d)" % (usrId, classId, number, level, status)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def modifyUsrClass(self, usrId=int(), classId=int(), number=int(), level=int(), status=int()):
        # Check if exists
        sql = "select * from usrClass where usrId = %d and classId = %d limit 1" % (usrId, classId)
        if self.db.execute(sql) == 0:
            return "can't find"

        sql = "update usrClass set number=%d, level=%d, status=%d where usrId=%d and classId=%d" % (number, level, status, usrId, classId)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    #
    def getUsrClassInfo(self, usrId=int(), classId=int()):
        sql = "select * from usrClass where usrId = %d and classId = %d limit 1" % (usrId, classId)
        self.db.execute(sql)
        row = self.db.cur.fetchone()
        if type(row) != type(None):
            if row.__len__()>0:
                return row
            else:
                return []
        else:
            return []

    #
    def getUsrClass(self, usrId=int()):
        sql = "select * from usrClass where usrId = %d" % usrId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__()>0:
                return row
            else:
                return []
        else:
            return []

    #
    def getClassUsr(self, classId=int()):
        sql = "select * from usrClass where classId = %d" % classId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if row.__len__() > 0 and type(row) != type(None):
            return row
        else:
            return []

    #
    def getClassUsrIn(self, classId=int()):
        sql = "select * from usrClass where classId = %d and status = 1" % classId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if row.__len__() > 0 and type(row) != type(None):
            return row
        else:
            return []

    #
    def deleteClassUsrByClassId(self, classId=int()):
        sql = "delete from usrClass where classId = %d" % classId
        self.db.execute(sql)
        self.db.con.commit()
        return "success"

    ########################################################################
    ########################################################################
    #classCourse
    def createClassCourseTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS classCourse (
                 classId INT(20) not null,
                 courseId INT(20) not null,
                 usrId INT(20) not null,
                 postDate VARCHAR (100) not null,
                 time INT (20) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertClassCourse(self, classId=int(), courseId=int(), usrId=int(), postDate=str(), time=int()):
        # Check if exists
        sql = "select * from classCourse where classId = %d and courseId = %d and postDate = '%s' limit 1" % (classId, courseId, postDate)
        if self.db.execute(sql) != 0:
            return "existed"

        sql = "insert into classCourse(classId, courseId, usrId, postDate, time) values(%d, %d, %d, '%s', %d)" % (classId, courseId, usrId, postDate, time)
        self.db.execute(sql)
        self.db.con.commit()
        return "success"
    
    #
    def getClassCourseInfo(self, classId=int()):
        sql = "select * from classCourse where classId = %d" % classId
        self.db.execute(sql)
        row = self.db.cur.fetchall()
        if type(row) != type(None):
            if row.__len__()>0:
                return row
            else:
                return []
        else:
            return []
        
    #
    def deleteClassCourseById(self, id = int()):
        sql = "select * from classCourse where id = %d limit 1" % id
        if self.db.execute(sql) != 1:
            return "not existed"

        sql = "delete from classCourse where id = %d" % id
        self.db.execute(sql)
        self.db.con.commit()
        return "success"
    ########################################################################
    ########################################################################
    #usrGrade
    def createUsrGradeTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS usrGrade (
                 usrId INT(20) not null,
                 role VARCHAR (100) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 primary key(id))"""
        self.db.execute(sql)

    #
    def insertUsrGrade(self, usrId=int(), role=str()):
        # Check if exists
        sql = "select * from usrGrade where usrId = %d limit 1" % usrId
        if self.db.execute(sql) != 0:
            print ("existed")
            return "existed"

        sql = "insert into usrGrade(usrId, role) values(%d,'%s')" % (usrId, role)
        self.db.execute(sql)
        self.db.con.commit()
        print ("success")
        return "success"

    #
    def getUsrGrade(self, usrId = int()):
        sql = "select * from usrGrade where usrId = %d limit 1" % usrId
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
    def getGradeUsr(self, role=str()):
        sql = "select * from usrGrade where role = '%s'" % role
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
    def getGradeById(self, id=int()):
        sql = "select * from usrGrade where id = %d limit 1" % id
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

if __name__ == '__main__':
    print("databaseTable")