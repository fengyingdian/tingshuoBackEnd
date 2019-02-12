# -*- coding: utf-8 -*-
# filename: handle.py

import database as db
import databaseTable as tb
import databaseRanking as rb
import time
import types
import os

#date = time.localtime()
#week = int(time.strftime("%W", date))
#weekday = int(time.strftime("%w", date)) + 1

class databaseManage:
    #
    def __init__(self):
        self.db = db.Edatabase()
        self.db.opendb()
        self.db.createUsrTable()
        self.db.createCourseTable()
        self.db.createPunchClockTable()
        self.db.createCommentTable()
        self.tb = tb.databaseTable(self.db)
        self.rb = rb.databaseRanking(self.db)

    #
    def close(self):
        self.db.closedb()

    #
    def addUser(self, openId=str(), nickName=str(), gender=int(), city=str(), province=str(), country=str(), language=str(), imageSrc = str()):
        self.db.insertUsr(openId, nickName, gender, city, province, country, language, imageSrc)
        id = self.db.getUsrId(openId)
        return id, self.db.getUsrInfo(id)

    #
    def modifyUser(self, id=str(), nickName=str(), gender=int(), city=str(), province=str(), country=str(), language=str(), imageSrc = str()):
        print("databaseManage:", imageSrc)
        return self.db.modifyUsr(id, nickName, gender, city, province, country, language, imageSrc)

    #
    def relogUser(self, openId=str(), nickName=str(), gender=int(), city=str(), province=str(), country=str(), language=str(), imageSrc=str()):
        id = self.db.getUsrId(openId)
        if (id == None):
            return self.addUser(openId, nickName, gender, city, province, country, language, imageSrc)
        else:
            return id, self.db.getUsrInfo(id)

    #
    def getUsrInfo(self, id = int()):
        return self.db.getUsrInfo(id)

    #
    def getUsrOpenId(self, id = int()):
        return self.db.getUsrOpenId(id)

    #
    def getUsrs(self):
        return self.db.getUsrs()

    #
    def addCourse(self, name, date, content, imageSrc, audioSrc, videoSrc, amIPASrc, brIPASrc, huaSrc, zhengSrc,voiceAmSrc,voiceBrSrc,voiceAmPicSrc,voiceBrPicSrc):
        self.db.insertCourse(name, date, content, imageSrc, audioSrc, videoSrc, amIPASrc, brIPASrc, huaSrc, zhengSrc,voiceAmSrc,voiceBrSrc,voiceAmPicSrc,voiceBrPicSrc)
        return str(self.db.getCourseId(date))

    #
    def getCourseById(self, courseId):
        return self.db.getCourseById(courseId)

    #
    def getCourse(self, date):
        return self.db.getCourse(date)

    #
    def getCourses(self):
        return self.db.getCourses()

    #
    def deleteCourse(self, courseId):
        return self.db.deleteCourseById(courseId)

    #
    def addPunchClock(self, courseId, usrId, time, audioSrc, thumb):
        self.db.insertPunchClock(courseId, usrId, time, audioSrc, thumb)
        return str(self.db.getPunchClockId(courseId, usrId))

    #
    def getPunchClockById(self, punchId):
        return self.db.getPunchClockById(punchId)

    #
    def getPunchClock(self, courseId, usrId):
        return self.db.getPunchClock(courseId, usrId)

    #
    def getPunchClocks(self):
        return self.db.getPunchClocks()

    #
    def getPunchClocksByCourseId(self, courseId):
        return self.db.getPunchClocksByCourseId(courseId)

    #
    def getPunchClocksByCourseId50(self, courseId):
        return self.db.getPunchClocksByCourseId50(courseId)

    #
    def getPunchClocksByUsrId(self, usrId):
        return self.db.getPunchClocksByUsrId(usrId)

    #
    def deletePunchClockById(self, punchId):
        return self.db.deletePunchClockById(punchId)

    #
    def addComment(self, punchId, usrId, time, type, content):
        self.db.insertComment(punchId, usrId, time, type, content)
        return str(self.db.getCommentId(punchId, usrId, time))

    #
    def getCommentById(self, commentId):
        return self.db.getCommentById(commentId)

	#
    def getCommentsByUsrId(self, usrId):
        return self.db.getCommentsByUsrId(usrId)
		
    #
    def getCommentsByPunchId(self, punchId):
        return self.db.getCommentsByPunchId(punchId)

    #
    def getComment(self, punchId, usrId, time):
        return self.db.getComment(punchId, usrId, time)

    #
    def getComments(self):
        return self.db.getComments()

    #
    def deleteCommentById(self, commentId):
        return self.db.deleteCommentById(commentId)

    #
    def deleteCommentsByPunchId(self, punchId):
        return self.db.deleteCommentsByPunchId(punchId)

    #
    def deleteCommentsByUsrId(self, punchId, usrId):
        return self.db.deleteCommentsByUsrId(punchId, usrId)

    #
    def deleteComment(self, punchId, usrId, time):
        return self.db.deleteComment(punchId, usrId, time)

    #
    def addClass(self, name = str(), sName = str(), type = int(), maxCount = int(), info = str(), coverSrc = str(), admittance = int(), punchLimit = int(), time = str(), usrId = int()):
        if (self.tb.insertClass(name, sName, type, maxCount, info, coverSrc, admittance, punchLimit, time, usrId) == "existed"):
            return "existed"
        res = self.tb.getClassBysName(sName, type)
        if(len(res) > 5):
            return str(res[5])

    #
    def modifyClass(self, name = str(), sName = str(), type = int(), maxCount = int(), info = str(), coverSrc = str(), admittance = int(), punchLimit = int(), usrId = int(), classId = int()):
        return self.tb.modifyClass(name, sName, type, maxCount, info, coverSrc, admittance, punchLimit, time, usrId, classId)

    #
    def deleteClassById(self, classId=int()):
        return self.tb.deleteClassById(classId)

    #
    def getClasses(self):
        return self.tb.getClasses()

    #
    def getClassBysName(self, sName = str(), type = int()):
        return self.tb.getClassBysName(sName, type)

    #
    def getClass(self, name = str(), sName = str(), type = int()):
        return self.tb.getClass(name, sName, type)

    #
    def getClassById(self, id = int()):
        return self.tb.getClassById(id)

    #
    def addUsrClass(self, usrId, classId, level=int(), status=int()):
        row = self.tb.getClassUsr(classId)
        if row == []:
            return self.tb.insertUsrClass(usrId, classId, 1, level, status)
        else:
            print("addUsrClass: ", row.__len__())
            return self.tb.insertUsrClass(usrId, classId, row.__len__() + 1, level, status)

    #
    def modifyUsrClass(self, usrId=int(), classId=int(), number=int(), level=int(), status=int()):
        return self.tb.modifyUsrClass(usrId, classId, number, level, status)

    #
    def getUsrClassInfo(self, usrId=int(), classId=int()):
        return self.tb.getUsrClassInfo(usrId, classId)

    #
    def getUsrClass(self, usrId=int()):
        return self.tb.getUsrClass(usrId)

    #
    def getClassUsr(self, classId=int()):
        return self.tb.getClassUsr(classId)

    #
    def getClassUsrIn(self, classId=int()):
        return self.tb.getClassUsrIn(classId)

    #
    def addClassCourse(self, classId=int(), courseId=int(), usrId=int(), postDate=str(), time=int()):
        return self.tb.insertClassCourse(classId, courseId, usrId, postDate, time)

    #
    def getClassCourseInfo(self, classId=int()):
        return self.tb.getClassCourseInfo(classId)

    #
    def deleteClassCourseById(self, id=int()):
        return self.tb.deleteClassCourseById(id)

    #
    def deleteClassUsrByClassId(self, classId=int()):
        return self.tb.deleteClassUsrByClassId(classId)

    #
    def addUsrGrade(self, usrId=int(), grade=str()):
        return self.tb.insertUsrGrade(usrId, grade)

    #
    def getUsrGrade(self, usrId=int()):
        return self.tb.getUsrGrade(usrId)

    #
    def getGradeUsr(self, grade=str()):
        return self.tb.getGradeUsr(grade)

    #
    def getGradeById(self, id=int()):
        return self.tb.getGradeById(id)
    #
    def insertFormId(self, openId=str(), formId=str()):
        return self.tb.insertFormId(openId, formId)

    def getValidFormId(self, openId=str()):
        return self.tb.getValidFormId(openId)

    def deleteFormId(self):
        return self.tb.deleteFormId()

    #
    def insertPunchRanking(self, date=str(), usrId=int(), punchTime=int(), commentTime=int(), rank=int(), time=int()):
        return self.rb.insertPunchRanking(date, usrId, punchTime, commentTime, rank, time)
    #
    def getPunchRanking(self, date=str()):
        return self.rb.getPunchRanking(date)

    #
    def insertCommentRanking(self, date=str(), usrId=int(), commentTime=int(), rank=int(), time=str()):
        return self.rb.insertCommentRanking(date, usrId, commentTime, rank, time)

    #
    def getcommentRanking(self, date=str()):
        return self.rb.getcommentRanking(date)

