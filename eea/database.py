#!/usr/bin/python
# -*- coding: UTF-8 -*-

import MySQLdb
import os
import re

import sys
reload(sys)
sys.setdefaultencoding('utf8')

#
class Edatabase:
    #
    def __init__(self):
        self.con = None
        self.cur = None

    #
    def opendb(self):
        #
        try:
            self.con = MySQLdb.connect(host='localhost', user='root', passwd='Qing660910', port=3306, charset="utf8")
            self.cur = self.con.cursor()
            self.cur.execute('create database if not EXISTS EEA CHARACTER SET UTF8')
            self.cur.execute('use EEA')

        except MySQLdb, e:
            print("Mysql Error %d: '%s'" % (e.args[0], e.args[1]))

    #
    def closedb(self):
        #
        try:
            self.cur.close()
            self.con.close()
        except MySQLdb, e:
            print("Mysql Error %d: '%s'" % (e.args[0], e.args[1]))

    #
    def execute(self, sql):
        try:
            return self.cur.execute(sql)
        except MySQLdb, e:
            print("Mysql Error %d: '%s'" % (e.args[0], e.args[1]))

    ########################################################################
    ########################################################################
    #usr
    def createUsrTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS usr (
                 openId VARCHAR (100) not null,
                 nickName VARCHAR (100) not null,
                 gender INT(20),
                 city VARCHAR (100) not null,
                 province VARCHAR (100) not null,
                 country VARCHAR (100) not null,
                 language VARCHAR (100) not null,
                 imageSrc VARCHAR (256) not null,
                 id INT(20) not null AUTO_INCREMENT,
                 primary key(id))"""
        self.execute(sql)

    #
    def insertUsr(self, openId = str(), nickName = str(), gender = int(), city = str(), province = str(), country = str(), language = str(), imageSrc = str()):
        #Check if exists
        sql = "select * from usr where openId = '%s' limit 1" % openId
        if self.execute(sql) != 0:
            print ("existed")
            return "existed"

        sql = "insert into usr(openId, nickName, gender, city, province, country, language, imageSrc) values('%s','%s',%d,'%s','%s','%s','%s','%s')" % (openId, nickName, gender, city, province, country, language, imageSrc)
        self.execute(sql)
        self.con.commit()
        print ("success")
        return "success"

    #
    def modifyUsr(self, id, nickName = str(), gender = int(), city = str(), province = str(), country = str(), language = str(), imageSrc = str()):
        #Check if exists
        sql = "select * from usr where id = %d limit 1" % id
        if self.execute(sql) == 0:
            print ("not existed")
            return "not existed"

        sql = "update usr set nickName='%s', gender=%d, city='%s', province='%s', country='%s', language='%s', imageSrc='%s' where id=%d" %(nickName, gender, city, province, country, language, imageSrc, id)
        self.execute(sql)
        self.con.commit()
        print ("success")
        return "success"

    #
    def getUsrInfo(self, id = int()):
        sql = "select * from usr where id = %d limit 1" % id
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getUsrNickName(self, id = int()):
        sql = "select * from usr where id = %d limit 1" % id
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() == 9:
                return row[1]
            else:
                return None
        else:
            return None

    #
    def getUsrOpenId(self, id = int()):
        sql = "select * from usr where id = %d limit 1" % id
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() == 9:
                return row[0]
            else:
                return None
        else:
            return None

    #
    def getUsrId(self, openId = str()):
        sql = "select * from usr where openId = '%s' limit 1" % openId
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() == 9:
                return row[8]
            else:
                return None
        else:
            return None

    #
    def getUsrs(self):
        sql = "select * from usr"
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    ########################################################################
    ########################################################################
    # course
    def createCourseTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS course(
                 name VARCHAR (100) not null,
                 date VARCHAR (100) not null,
                 content VARCHAR (256) not null,
                 imageSrc VARCHAR (512) not null,
                 audioSrc VARCHAR (512) not null,
                 videoSrc VARCHAR (512) not null,
                 amIPASrc VARCHAR (512) not null,
                 brIPASrc VARCHAR (512) not null,
                 huaSrc VARCHAR (512) not null,
                 zhengSrc VARCHAR (512) not null,
                 id INT(20) not null AUTO_INCREMENT,
				 voiceAmSrc VARCHAR (512) not null,
                 voiceBrSrc VARCHAR (512) not null,
				 voiceAmPICSrc VARCHAR (512) not null,
                 voiceBrPICSrc VARCHAR (512) not null,
                 primary key(id))"""
        self.execute(sql)

    #
    def insertCourse(self, name, date, content, imageSrc, audioSrc, videoSrc, amIPASrc,brIPASrc,huaSrc,zhengSrc,voiceAmSrc,voiceBrSrc,voiceAmPicSrc,voiceBrPicSrc):
        sql = "select * from course where date = '%s' limit 1" % date
        if self.execute(sql) != 0:
            sql = "update course set content='%s', imageSrc='%s', audioSrc='%s', videoSrc='%s', amIPASrc='%s', brIPASrc='%s', huaSrc='%s', zhengSrc='%s', voiceAmSrc='%s', voiceBrSrc='%s', voiceAmPicSrc='%s', voiceBrPicSrc='%s' where date='%s' " % (content, imageSrc, audioSrc, videoSrc, amIPASrc, brIPASrc, huaSrc, zhengSrc, voiceAmSrc, voiceBrSrc, voiceAmPicSrc, voiceBrPicSrc, date)
            self.execute(sql)
            self.con.commit()
            return "existed"

        sql = "insert into course(name, date, content, imageSrc, audioSrc, videoSrc, amIPASrc, brIPASrc, huaSrc, zhengSrc,voiceAmSrc,voiceBrSrc,voiceAmPicSrc,voiceBrPicSrc) values('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (name, date, content, imageSrc, audioSrc, videoSrc, amIPASrc, brIPASrc, huaSrc, zhengSrc, voiceAmSrc, voiceBrSrc, voiceAmPicSrc, voiceBrPicSrc)
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deleteCourse(self, date):
        sql = "select * from course where date = '%s' limit 1" % date
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from course where date = '%s'" % date
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deleteCourseById(self, id):
        sql = "select * from course where id = %d limit 1" % id
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from course where id = %d" % id
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def getCourseById(self, id):
        sql = "select * from course where id = %d limit 1" % id
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getCourse(self, date):
        sql = "select * from course where date = '%s'" % date
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getCourseId(self, date):
        sql = "select * from course where date = '%s'" % date
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row[5]
            else:
                return None
        else:
            return None

    #
    def getCourses(self):
        sql = "select * from course"
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    ########################################################################
    ########################################################################
    # punchClock
    def createPunchClockTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS punchClock (
                 courseId INT (20),
                 usrId INT (20),
                 time VARCHAR (100) not null,
                 audioSrc VARCHAR (512) not null,
                 thumb INT (20),
                 id INT(20) AUTO_INCREMENT,
				 practice INT (20),
				 content VARCHAR (1024) not null,
				 score VARCHAR (100) not null,
                 primary key(id))"""
        self.execute(sql)

    #
    def insertPunchClock(self, courseId, usrId, time, audioSrc, thumb, practice, content, score):
        sql = "select * from punchClock where courseId = %d and usrId = %d limit 1" % (courseId, usrId)
        if self.execute(sql) != 0:
            return "existed"

        sql = "insert into punchClock(courseId, usrId, time, audioSrc, thumb, practice, content, score) values(%d, %d, '%s','%s', %d, %d, '%s', '%s')" % (courseId, usrId, time, audioSrc, thumb, practice, content, score)
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deletePunchClock(self, courseId, usrId):
        sql = "select * from punchClock where courseId = %d and usrId = %d limit 1" % (courseId, usrId)
        if self.execute(sql) != 1:
            return "not existed!"

        sql = "delete from punchClock where courseId = %d and usrId = %d" % (courseId, usrId)
        self.execute(sql)
        self.con.commit()
        return "success!"

    #
    def deletePunchClockById(self, id):
        sql = "select * from punchClock where id = %d limit 1" % id
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from punchClock where id = %d" % id
        self.execute(sql)
        self.con.commit()
        print("success")
        return "success"

    #
    def getPunchClock(self, courseId, usrId):
        sql = "select * from punchClock where courseId = %d and usrId = %d" % (courseId, usrId)
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getPunchClockId(self, courseId, usrId):
        sql = "select * from punchClock where courseId = %d and usrId = %d" % (courseId, usrId)
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row[5]
            else:
                return None
        else:
            return None

    #
    def getPunchClockById(self, id):
        sql = "select * from punchClock where id = %d" % id
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getPunchClocks(self):
        sql = "select * from punchClock"
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getPunchClocksByCourseId(self, courseId):
        sql = "select * from punchClock where courseId = %d" % courseId
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getPunchClocksByCourseId50(self, courseId):
        sql = "select * from punchClock where courseId = %d limit 50" % courseId
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getPunchClocksByUsrId(self, usrId = int()):
        sql = "select * from punchClock where usrId = %d" % usrId
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []
    ########################################################################
    ########################################################################
    # comment
    def createCommentTable(self):
        # 创建数据表SQL语句
        sql = """CREATE TABLE if not EXISTS comment (
                 punchId INT(20),
                 usrId INT(20),
                 time VARCHAR (100) not null,
                 type INT(20),
                 content VARCHAR (1024) not null,
                 thumb INT (20),
                 id INT(20) AUTO_INCREMENT,
                 toUsrId INT(20),
                 primary key(id))"""
        self.execute(sql)

    #
    def insertComment(self, punchId, usrId, time, type, content, toUsrId):
        sql = "insert into comment(punchId, usrId, time, type, content, thumb, toUsrId) values(%d,%d,'%s',%d,'%s',0, %d)" % (punchId, usrId, time, type, content, toUsrId)
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deleteCommentsByPunchId(self, punchId):
        sql = "select * from comment where punchId = %d" % punchId
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from comment where punchId = %d" % punchId
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deleteCommentsByUsrId(self, punchId, usrId):
        sql = "select * from comment where punchId = %d and usrId = %d" % (punchId, usrId)
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from comment where punchId = %d and usrId = %d" % (punchId, usrId)
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deleteComment(self, punchId, usrId, time):
        sql = "select * from comment where punchId = %d and usrId = %d and time = '%s' limit 1" % (punchId, usrId, time)
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from comment where punchId = %d and usrId = %d and time = '%s'" % (punchId, usrId, time)
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def deleteCommentById(self, id):
        sql = "select * from comment where id = %d limit 1" % id
        if self.execute(sql) != 1:
            return "not existed"

        sql = "delete from comment where id = %d" % id
        self.execute(sql)
        self.con.commit()
        return "success"

    #
    def getComment(self, punchId, usrId, time):
        sql = "select * from comment where punchId = %d and usrId = %d and time = '%s'" % (punchId, usrId, time)
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getCommentId(self, punchId, usrId, time):
        sql = "select * from comment where punchId = %d and usrId = %d and time = '%s'" % (punchId, usrId, time)
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row[6]
            else:
                return None
        else:
            return None

    #
    def getCommentById(self, id):
        sql = "select * from comment where id = %d" % id
        self.execute(sql)
        row = self.cur.fetchone()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getCommentsByPunchId(self, punchId):
        sql = "select * from comment where punchId = %d" % punchId
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []
			
    #
    def getCommentsByUsrId(self, usrId):
        sql = "select * from comment where usrId = %d" % usrId
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []

    #
    def getComments(self):
        sql = "select * from comment"
        self.execute(sql)
        row = self.cur.fetchall()
        if type(row) != type(None):
            if row.__len__() >= 1:
                return row
            else:
                return []
        else:
            return []


if __name__ == '__main__':
    db = Edatabase()
    db.opendb()
    print(db.getUsrs())
    #

    db.closedb()