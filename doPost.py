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

from wxServer import wxServer

class doPost(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr
        reload(doFun)
        self.doFun = doFun.doFun(dbMgr)

    def do(self, data, webData):
        try:
            if (int(data["usrId"]) < 1):
                return json.dumps({"res": "wrong usrId!"})
            if (data["type"] == "1200"):
                return self.do1200(data, webData)
            elif(data["type"] == "1300"):
                return self.do1300(data, webData)
            elif(data["type"] == "1500"):
                return self.do1500(data, webData)
            elif (data["type"] == "1501"):
                return self.do1501(data, webData)
        except Exception, Argument:
            return json.dumps({"res": "error: " + str(Argument)})

    def do1200(self,data, webData):
        if (data["class"] == "1" or data["class"] == "2"):
            return json.dumps({"res": "not allow!"})

        if (self.doFun.checkFileAudio(webData) == False):
            return json.dumps({"res": "can't find ftypM4A/ftypmp42."})

        if (data.has_key("thumb") == False):
            data["thumb"] = 0

        localtime = time.asctime(time.localtime(time.time()))
        data["time"] = localtime
        punchId = self.dbMgr.addPunchClock(int(data["courseId"]), int(data["usrId"]), data["time"], "",
                                           int(data["thumb"]))
        print("1200: punchId:", punchId)
        path = "./static/class/" + data["date"] + "/" + punchId + "/"
        file = "punch.m4a"
        if (self.doFun.saveFileAudio(webData, path, file) == True):
            return self.doFun.getCourse(data)
        else:
            return json.dumps({"res": "save failed!"})

    def do1300(self, data, webData):
        if (self.doFun.checkFileAudio(webData) == False):
            return json.dumps({"res": "can't find ftypM4A/ftypmp42."})

        value = self.dbMgr.getPunchClockById(int(data["punchId"]))
        if (type(value) == type(None)):
            return json.dumps({"res": "deleted"})

        localtime = time.asctime(time.localtime(time.time()))
        data["time"] = localtime
        data["content"] = "语音"

        commentId = self.dbMgr.addComment(int(data["punchId"]), int(data["usrId"]), data["time"], 2, "")
        print("1300: commentId:", commentId)

        path = "./static/class/" + data["date"] + "/" + data["punchId"] + "/"
        name = commentId + ".m4a"
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