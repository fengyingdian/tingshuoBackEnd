# -*- coding: utf-8 -*-
# filename: doCourse1.py

import utils

import requests

import json

#
try:
  import cookielib
except:
  import http.cookiejar as cookielib

import web

import utils

from WXBizDataCrypt import WXBizDataCrypt

import datetime

import time

import doFun

from wxServer import wxServer

class doCourse1(object):
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr
        reload(doFun)
        self.doFun = doFun.doFun(dbMgr)

    def do(self, data, webData):
        try:
            if (data["type"] == "1200"):
                return self.do1200(data, webData)
            elif(data["type"] == "1300"):
                return self.do1300(data, webData)
        except Exception, Argument:
            return json.dumps({"res": "error: " + str(Argument)})

    def do1100(self, data):
        id = self.dbMgr.addCourse(data["name"], data["date"], data["content"], data["imageSrc"], data["audioSrc"],
                                  data["videoSrc"], data["amIPASrc"], data["brIPASrc"], data["huaSrc"],
                                  data["zhengSrc"], data["voiceAmSrc"], data["voiceBrSrc"], data["voiceAmPicSrc"],
                                  data["voiceBrPicSrc"])
        return json.dumps({"res": "success", "courseId": id})

    def do1101(self, data):
        resData = self.dbMgr.getCourseById(int(data["courseId"]))
        return json.dumps({"res": "success", "data": resData})

    def do1111(self, data):
        resData = self.dbMgr.getCourse(data["date"])
        return json.dumps({"res": "success", "data": resData})

    def do1102(self, data):
        return self.doFun.getCourse(data)

    def do1103(self, data):
        topShows = [{
            "name": '每日英语',
            "info": "由EEA全体老师共同打造的以详细讲解英美影视剧经典片段为主，每天一更的经典课程，累计参与打卡人次已经超过10w，快来加入我们吧！",
        }, {
            "name": '音标基础强化课',
            "info": "由Lemon老师耗时半年，精心打磨的美音音标课程，即将开启报名通道，敬请期待！详情咨询Joooy（微信号：race_joy 或 go_for_dreams）",
        }]
        resData = self.dbMgr.getCourses()
        if type(resData) == type(None):
            return json.dumps({"res": "success", "data": [], "topShows": topShows})
        res = self.dbMgr.getUsrGrade(int(data["usrId"]))
        nowDate = datetime.datetime.now().strftime('%Y%m%d')
        if (type(res) != type(None)):
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=1)
            newDate = now + delta
            nowDate = newDate.strftime('%Y%m%d')
        courseData = []
        if data["usrId"] == "1":
            courseData = resData
        else:
            for index, value in enumerate(resData):
                if (value[1] <= nowDate):
                    courseData.append(value)
        return json.dumps({"res": "success", "data": courseData, "topShows": topShows})

    def do1104(self, data):
        self.dbMgr.deleteCourse(int(data["courseId"]))
        return json.dumps({"res": "success"})

    def do1201(self, data):
        resData = self.dbMgr.getPunchClockById(int(data["punchId"]))
        return json.dumps({"res": "success", "data": resData})

    def do1202(self, data):
        resData = self.dbMgr.getPunchClock(int(data["courseId"]), int(data["usrId"]))
        if (resData == []):
            return json.dumps({"res": "fail"})
        return json.dumps({"res": "success", "punchData": resData})

    def do1203(self, data):
        resData = self.dbMgr.getPunchClocks()
        return json.dumps({"res": "success", "data": resData})

    def do1204(self, data):
        # save new formId
        userOpenId = self.dbMgr.getUsrOpenId(int(data["usrId"]))
        print("1204: insertFormId ", self.dbMgr.insertFormId(userOpenId, data["formId"]))
        #
        res = self.dbMgr.deletePunchClockById(int(data["punchId"]))
        print("1204: deletePunchClockById: ", res)
        res = self.dbMgr.deleteCommentsByPunchId(int(data["punchId"]))
        print("1204: deleteCommentsByPunchId: ", res)
        #
        return self.doFun.getCourse(data)

    def do1205(self, data):
        usrInfo = self.dbMgr.getUsrInfo(int(data["punchHostId"]))
        punches = self.dbMgr.getPunchClocksByUsrId(int(data["punchHostId"]))
        resData = []
        for i in range(len(punches)):
            onePunch = punches[i]
            oneCourse = self.dbMgr.getCourseById(onePunch[0])
            if(oneCourse == []):
                continue
            oneData = {
                "name": oneCourse[0],
                "date": oneCourse[1],
                "content": oneCourse[2],
                "punchId": onePunch[5],
                "punchTime": onePunch[2],
                "index": i+1,
            }
            resData.append(oneData)
        return json.dumps({"res": "success", "data": resData, "usrInfo": usrInfo})

    def do1300(self, data):
        value = self.dbMgr.getPunchClockById(int(data["punchId"]))
        if (value == []):
            return json.dumps({"res": "deleted"})
        localtime = time.asctime(time.localtime(time.time()))
        data["time"] = localtime
        commentId = self.dbMgr.addComment(int(data["punchId"]), int(data["usrId"]), data["time"], 1, data["content"])
        print("1300 commentId: ", commentId)
        if type(commentId) == type(None):
            return json.dumps({"res": "fail", "commentData": []})
        return self.doFun.dealNewComment(data)

    def do1301(self, data):
        resData = self.dbMgr.getCommentById(int(data["commentId"]))
        return json.dumps({"res": "success", "data": resData})

    def do1302(self, data):
        resData = self.dbMgr.getComment(int(data["punchId"]), int(data["usrId"]))
        return json.dumps({"res": "success", "data": resData})

    def do1303(self, data):
        resData = self.dbMgr.getComments()
        return json.dumps({"res": "success", "data": resData})

    def do1304(self, data):
        course = self.dbMgr.getCourse(data["date"])
        value = self.dbMgr.getPunchClockById(int(data["punchId"]))
        if (value == []):
            return json.dumps({"res": "deleted"})
        usrInfo = self.dbMgr.getUsrInfo(value[1])
        usr = {}
        if(usrInfo != []):
            usr = {
                "name": usrInfo[1],
                "image": usrInfo[7],
                "time": value[2],
                "content": course[2],
                "audio": value[3],
                "thumb": value[4],
                "punchId": value[5],
                "usrId": value[1],
                "date": data["date"],
                "courseId": course[10],
            }
        else:
            usr = {
                "name": "unknow",
                "image": "../image/button/tourist.jpg",
                "time": value[2],
                "content": course[2],
                "audio": value[3],
                "thumb": value[4],
                "punchId": value[5],
                "usrId": value[1],
                "date": data["date"],
                "courseId": course[10],
            }
        # get usr grade
        resGrade = self.dbMgr.getUsrGrade(value[1])
        if resGrade != []:
            usr["role"] = resGrade[1]
        else:
            usr["role"] = "None"
        commentData = self.dbMgr.getCommentsByPunchId(int(data["punchId"]))
        if commentData != []:
            resData = self.doFun.getComments(data, commentData)
            return json.dumps({"res": "success", "usr": usr, "commentData": resData})
        else:
            return json.dumps({"res": "success", "usr": usr, "commentData": []})

    def do1305(self, data):
        value = self.dbMgr.getPunchClockById(int(data["punchId"]))
        if (value == []):
            return json.dumps({"res": "deleted"})
        res = self.dbMgr.deleteCommentById(int(data["commentId"]))
        commentData = self.dbMgr.getCommentsByPunchId(int(data["punchId"]))
        if commentData != []:
            resData = self.doFun.getComments(data, commentData)
            return json.dumps({"res": "success", "commentData": resData})
        else:
            return json.dumps({"res": "success", "commentData": []})

    def do1306(self, data):
        usrInfo = self.dbMgr.getUsrInfo(int(data["commentHostId"]))
        comments = self.dbMgr.getCommentsByUsrId(int(data["commentHostId"]))
        resData = []
        for i in range(len(comments)):
            oneComment = comments[i]
            onePunch = self.dbMgr.getPunchClockById(oneComment[0])
            if(onePunch == []):
                continue
            oneCourse = self.dbMgr.getCourseById(onePunch[0])
            if(oneCourse == []):
                continue
            oneUsr = self.dbMgr.getUsrInfo(onePunch[1])
            if(oneUsr == []):
                oneData = {
                    "name": oneCourse[0],
                    "date": oneCourse[1],
                    "content": oneCourse[2],
                    "punchId": onePunch[5],
                    "usrName": "unknow",
                    "usrImage": "../image/button/tourist.png",
                    "index": i + 1,
                }
            else:
                oneData = {
                    "name": oneCourse[0],
                    "date": oneCourse[1],
                    "content": oneCourse[2],
                    "punchId": onePunch[5],
                    "usrName": oneUsr[1],
                    "usrImage": oneUsr[7],
                    "index": i+1,
                }
            resData.append(oneData)
        return json.dumps({"res": "success", "data": resData, "usrInfo": usrInfo})