# -*- coding: utf-8 -*-
# filename: doGet.py

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
import doOthers
import doCourse1

from wxServer import wxServer

class doGet(object):
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr
        reload(doFun)
        self.doFun = doFun.doFun(dbMgr)
        reload(doOthers)
        self.doOthers = doOthers.doOthers(dbMgr)
        reload(doCourse1)
        self.doCourse1 = doCourse1.doCourse1(dbMgr)

    def do(self, data):
        try:
            # register
            if (data["type"] == "1000"):
                return self.doOthers.do1000(data)

            if (int(data["usrId"]) < 1):
                return json.dumps({"res": "wrong usrId!"})
            # get all courses
            elif (data["type"] == "0000"):
                return self.doOthers.do0000(data)
            # get all courses
            elif (data["type"] == "0001"):
                return self.doOthers.do0001(data)
            # get all classes
            elif (data["type"] == "0002"):
                return self.doOthers.do0002(data)
            # get punch ranking
            elif (data["type"] == "0003"):
                return self.doOthers.do0003(data)
            # get comment ranking
            elif (data["type"] == "0004"):
                return self.doOthers.do0004(data)
            # get ranking
            elif (data["type"] == "0005"):
                return self.doOthers.do0005(data)
            # register
            elif (data["type"] == "1001"):
                return self.doOthers.do1001(data)
            elif (data["type"] == "1002"):
                return self.doOthers.do1002(data)
            elif (data["type"] == "1003"):
                return self.doOthers.do1003(data)
            # upload course
            elif (data["type"] == "1100"):
                return self.doCourse1.do1100(data)
            # get course by id
            elif (data["type"] == "1101"):
                return self.doCourse1.do1101(data)
            # get course
            elif (data["type"] == "1111"):
                return self.doCourse1.do1111(data)
            # get course
            elif (data["type"] == "1102"):
                return self.doCourse1.do1102(data)
            # get courses
            elif (data["type"] == "1103"):
                return self.doCourse1.do1103(data)
            # delete course
            elif (data["type"] == "1104"):
                return self.doCourse1.do1104(data)
            # get punchClock
            elif (data["type"] == "1201"):
                return self.doCourse1.do1201(data)
            # get punchClock
            elif (data["type"] == "1202"):
                return self.doCourse1.do1202(data)
            # get punchClocks
            elif (data["type"] == "1203"):
                return self.doCourse1.do1203(data)
            # delete punchClock
            elif (data["type"] == "1204"):
                return self.doCourse1.do1204(data)
            # get punchClock by usrId
            elif (data["type"] == "1205"):
                return self.doCourse1.do1205(data)
            # upload comment
            elif (data["type"] == "1300"):
                return self.doCourse1.do1300(data)
            # get comment by id
            elif (data["type"] == "1301"):
                return self.doCourse1.do1301(data)
            # get comment
            elif (data["type"] == "1302"):
                return self.doCourse1.do1302(data)
            # get comments
            elif (data["type"] == "1303"):
                return self.doCourse1.do1303(data)
            # get comments
            elif (data["type"] == "1304"):
                return self.doCourse1.do1304(data)
            # delete comment
            elif (data["type"] == "1305"):
                return self.doCourse1.do1305(data)
            # get comments by usrId
            elif (data["type"] == "1306"):
                return self.doCourse1.do1306(data)
            # add usrGrade
            elif (data["type"] == "1400"):
                return self.doOthers.do1400(data)
            # get usrGrade
            elif (data["type"] == "1401"):
                return self.doOthers.do1401(data)
            # add class
            elif (data["type"] == "1500"):
                return self.doOthers.do1500(data)
            # check class
            elif (data["type"] == "1501"):
                return self.doOthers.do1501(data)
            # apply VIP class
            elif (data["type"] == "1502"):
                return self.doOthers.do1502(data)
            # get usr class info
            elif (data["type"] == "1503"):
                return self.doOthers.do1503(data)
            # get class info
            elif (data["type"] == "1504"):
                return self.doOthers.do1504(data)
            # add class course
            elif (data["type"] == "1505"):
                return self.doOthers.do1505(data)
            # get class course
            elif (data["type"] == "1506"):
                return self.doOthers.do1506(data)
            # apply class
            elif (data["type"] == "1507"):
                return self.doOthers.do1507(data)
            # modify classusr
            elif (data["type"] == "1508"):
                return self.doOthers.do1508(data)
            # delete class course
            elif (data["type"] == "1509"):
                return self.doOthers.do1509(data)
            # delete class
            elif (data["type"] == "1510"):
                return self.doOthers.do1510(data)
            # get punch times
            elif (data["type"] == "8001"):
                return self.doOthers.do8001(data)
            # get share group info
            elif (data["type"] == "9001"):
                return self.doOthers.do9001(data)
            # saveopts formId
            elif (data["type"] == "9002"):
                return self.doOthers.do9002(data)
        except Exception, Argument:
            return json.dumps({"res": "error: " + str(Argument)})