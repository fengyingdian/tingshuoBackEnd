# -*- coding: utf-8 -*-
# filename: doPost.py

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
import doFun2
import doFun3

from wxServer import wxServer

class doPost(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr
        reload(doFun)
        self.doFun = doFun.doFun(dbMgr)
        reload(doFun2)
        self.doFun2 = doFun2.doFun2(dbMgr)
        reload(doFun3)
        self.doFun3 = doFun3.doFun3(dbMgr)

    def do(self, data, webData):
        try:
            if (int(data["usrId"]) < 1):
                return json.dumps({"res": "wrong usrId!"})
            if (data["type"] == "1200"):
                return self.do1200(data, webData)
            elif(data["type"] == "1201"):
                return self.do1201(data, webData)
            elif(data["type"] == "1300"):
                return self.do1300(data, webData)
            elif(data["type"] == "1500"):
                return self.do1500(data, webData)
            elif (data["type"] == "1501"):
                return self.do1501(data, webData)
        except Exception, Argument:
            return json.dumps({"res": "error: " + str(Argument)})

    def do1200(self,data, webData):
        if (self.doFun.checkFileAudio(webData) == False):
            return json.dumps({"res": "can't find audio."})

        oldPunch = self.dbMgr.getPunchClock(int(data["courseId"]), int(data["usrId"]))
        if(oldPunch != []):
            #
            res = self.dbMgr.deletePunchClockById(oldPunch[5])
            res = self.dbMgr.deleteCommentsByPunchId(oldPunch[5])
            #
            # 20001 - 删除打卡(-5)
            self.doFun2.addFlowerEvent(int(data["usrId"]), 20001, -5, int(time.time()))

        if (data.has_key("content") == False):
            data["content"] = "-"
        if (data.has_key("practice") == False):
            data["practice"] = 0
        if (data.has_key("thumb") == False):
            data["thumb"] = 0
        if (data.has_key("score") == False):
            data["score"] = "-1"

        localtime = time.time()
        formattime = time.asctime(time.localtime(time.time()))
        data["time"] = formattime

        punchId = self.dbMgr.addPunchClock(int(data["courseId"]), int(data["usrId"]), data["time"], "",
                                           int(data["thumb"]), int(data["practice"]), data["content"], data["score"])

        #10001 - 打卡(5)
        self.doFun2.addFlowerEvent(int(data["usrId"]),10001,5,int(localtime))

        print("1200: punchId:", punchId)
        path = "./static/class/" + data["date"] + "/" + punchId + "/"
        file = "punch.m4a"
        if (self.doFun.saveFileAudio(webData, path, file) == True):
            return self.doFun.getCourse2(data)
        else:
            return json.dumps({"res": "save failed!"})

    def do1201(self, data, webData):
        formattime1 = time.asctime(time.localtime(time.time()))

        if (self.doFun.checkFileAudio(webData) == False):
            return json.dumps({"res": "can't find ftypM4A/ftypmp42."})

        courseData = self.dbMgr.getCourseById(int(data["courseId"]))
        if(courseData == []):
            return json.dumps({"res": "course error"})

        path = "./static/class/" + data["date"] + "/"
        file = data["usrId"] + "_" + data["path"] + ".m4a"

        if (self.doFun.saveFileAudio(webData, path, file) == True):
            return json.dumps({"res": "success"})
        else:
            return json.dumps({"res": "save failed!"})

    def do1300(self, data, webData):
        if (self.doFun.checkFileAudio(webData) == False):
            return json.dumps({"res": "can't find audio."})

        value = self.dbMgr.getPunchClockById(int(data["punchId"]))
        if (type(value) == type(None)):
            return json.dumps({"res": "deleted"})

        if (data.has_key("content") == False):
            data["content"] = "-"
        if(data.has_key("toUsrId") == False):
            data["toUsrId"] = 0
        if (data.has_key("contentType") == False):
            data["contentType"] = 2
        else:
            data["contentType"] = 3

        localtime = time.time()
        formattime = time.asctime(time.localtime(localtime))
        data["time"] = formattime

        commentId = self.dbMgr.addComment(int(data["punchId"]), int(data["usrId"]), data["time"], data["contentType"], data["content"], int(data["toUsrId"]))

        #10002-语音点评(3)
        self.doFun2.addFlowerEvent(int(data["usrId"]),10002,3,int(localtime))

        path = "./static/class/" + data["date"] + "/" + data["punchId"] + "/"
        name = commentId
        if(data["contentType"] == 2):
            name = name + ".m4a"
        else:
            name = name + ".mp3"
        if (self.doFun.saveFileAudio(webData, path, name) == True):
            return self.doFun.dealNewComment(data)
        else:
            return json.dumps({"res": "save failed!"})

    def do1500(self, data, webData):
        if (self.doFun.checkFileImage(webData) == False):
            return json.dumps({"res": "wrong type"})

        localtime = time.asctime(time.localtime(time.time()))
        data["time"] = localtime
        res = self.dbMgr.addClass(data["name"], data["sName"], int(data["classType"]), int(data["maxCount"]), data["info"],data["coverSrc"],int(data["admittance"]),int(data["punchLimit"]),data["time"],int(data["usrId"]))
        if(res == "existed"):
            return json.dumps({"res": res})
        self.dbMgr.addUsrClass(int(data["usrId"]), int(res), level=9, status=1)

        path = "./static/group/" + res + "/"
        if (self.doFun.saveFileImage(webData, path, "c") == True):
            calsses = self.doFun.getClasses(data)
            return json.dumps({"res": "success", "calsses": calsses})
        else:
            return json.dumps({"res": "save failed!"})

    def do1501(self, data, webData):
        if (self.doFun.checkFileImage(webData) == False):
            return json.dumps({"res": "wrong type"})

        path = "./static/group/" + data["classId"] + "/"
        if (self.doFun.saveFileImage(webData, path, "o") == True):
            return json.dumps({"res": "success"})
        else:
            return json.dumps({"res": "save failed!"})