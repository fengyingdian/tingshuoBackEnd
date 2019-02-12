# -*- coding: utf-8 -*-
# filename: doFun.py

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

from wxServer import wxServer

class doFun2(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr

    #add flower event
    def addFlowerEvent(self, usrId, eventCode, count, localTime):
        res = self.dbMgr.addFlowerEvent(usrId, 0, eventCode, count, localTime)
        if(res == "existed"):
            return
        self.dbMgr.modifyFlower(usrId, count)

    #add flower event
    def addFlowerEvent2(self, usrId, toUsrId, eventCode, count, localTime):
        res = self.dbMgr.addFlowerEvent(usrId, toUsrId, eventCode, count, localTime)
        if(res == "existed"):
            return
        self.dbMgr.modifyFlower(usrId, count)

    #add comment book event
    def addCommentBookEvent(self, usrId, toUsrId, punchId, eventCode, count, localTime):
        res = self.dbMgr.addCommentBookEvent(usrId, toUsrId, punchId, eventCode, count, localTime)
        if(res == "existed"):
            return "existed"
        self.dbMgr.modifyFlower(usrId, -count)
        return "success"

    #modify comment book event
    def modifyCommentBookEvent(self, usrId, toUsrId, punchId, eventCode, count, localTime):
        res = self.dbMgr.modifyCommentBookEvent(usrId, toUsrId, punchId, eventCode, localTime)
        if(res == "not existed"):
            return "not existed", 0

        #[eventCode]-[event]: 30000-预约等待中，30001-已点评，30002-被拒绝，30003-已超时，30004-已取消(目前不开放)
        if(eventCode == 30001):
            res, sum = self.dbMgr.modifyFlower(toUsrId, count)
        elif(eventCode == 30002 or eventCode == 30003):
            res, sum = self.dbMgr.modifyFlower(usrId, count)
        return res, sum