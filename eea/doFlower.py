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

import doFun2

import time

from wxServer import wxServer

class doFlower(object):
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr
        reload(doFun2)
        self.doFun2 = doFun2.doFun2(dbMgr)

    # 充值
    def do7000(self, data):
        usrInfo = self.dbMgr.getUsrInfo(int(data["chargeUsrId"]))
        if(usrInfo == []):
            return json.dumps({"res": "no usr"})

        localTime = time.time()
        res = self.dbMgr.addFlowerEvent(int(data["chargeUsrId"]), 0, 10000, int(data["count"]), int(localTime))
        if(res == "existed"):
            return json.dumps({"res": "existed"})

        resCode, sum = self.dbMgr.modifyFlower(int(data["chargeUsrId"]), int(data["count"]))
        return json.dumps({"res": resCode, "sum": sum, "name": usrInfo[1]})

    # 打赏
    def do7001(self, data):
        sum = self.dbMgr.getFlower(int(data["usrId"]))
        if(sum == []):
            return json.dumps({"res": "NE", "sum": 0})

        if(sum[1] < int(data["count"])):
            return json.dumps({"res": "NE", "sum": sum[1]})

        localTime = time.time()
        #打赏
        self.doFun2.addFlowerEvent2(int(data["usrId"]), int(data["toUsrId"]), 20005,-int(data["count"]),int(localTime))
        #被打赏
        self.doFun2.addFlowerEvent2(int(data["toUsrId"]), int(data["usrId"]), 10005, int(data["count"]), int(localTime))
        return json.dumps({"res": "success", "sum": sum[1]-int(data["count"])})

    # 账单
    def do7100(self, data):
        sum = self.dbMgr.getFlower(int(data["usrId"]))
        events = self.dbMgr.getFlowerEventByUsrId(int(data["usrId"]))
        return json.dumps({"res": "success", "sum": sum, "events": events})

    # 预约点评
    def do7200(self, data):
        sum = self.dbMgr.getFlower(int(data["usrId"]))
        if (sum == []):
            return json.dumps({"res": "NE", "sum": 0})

        if (sum[1] < int(data["count"])):
            return json.dumps({"res": "NE", "sum": sum[1]})

        localTime = time.time()
        res = self.doFun2.addCommentBookEvent(int(data["usrId"]), int(data["toUsrId"]), int(data["punchId"]), 30000, int(data["count"]), int(localTime))
        return json.dumps({"res": res, "sum": sum[1]-int(data["count"])})

    # 修改预约信息
    def do7201(self, data):
        localTime = time.time()
        res, sum = self.doFun2.modifyCommentBookEvent(int(data["bookUsrId"]), int(data["toUsrId"]), int(data["punchId"]), int(data["eventCode"]), int(data["count"]), int(localTime))
        return json.dumps({"res": res, "sum": sum})

   # 预约事件
    def do7300(self, data):
        eventStatus = {
            "30000": "待处理",
            "30001": "已点评",
            "30002": "已拒绝",
            "30003": "已超时",
            "30004": "已取消",
        }
        events1 = self.dbMgr.getCommentBookEventByUsrId(int(data["usrId"]))
        eventsRes1 = []
        for i in range(len(events1)):
            usrInfo = self.dbMgr.getUsrInfo(events1[i][1])
            if(usrInfo == []):
                continue
            punchClock = self.dbMgr.getPunchClockById(events1[i][2])
            if(punchClock == []):
                continue
            course = self.dbMgr.getCourseById(punchClock[0])
            if(course == []):
                continue
            oneEvent = {
                "usrName": usrInfo[1],
                "usrImage": usrInfo[7],
                "usrId": usrInfo[8],
                "time1": time.asctime(time.localtime(events1[i][5])),
                "time2": time.asctime(time.localtime(events1[i][6])),
                "eventCode": events1[i][3],
                "eventStatus": eventStatus[str(events1[i][3])],
                "courseTitle": course[0],
                "courseName": course[1],
                "courseContent": course[2],
                "punchId":events1[i][2],
                "count": events1[i][4],
            }
            eventsRes1.append(oneEvent)

        events2 = self.dbMgr.getCommentBookEventByToUsrId(int(data["usrId"]))
        eventsRes2 = []
        for i in range(len(events2)):
            usrInfo = self.dbMgr.getUsrInfo(events2[i][0])
            if(usrInfo == []):
                continue
            punchClock = self.dbMgr.getPunchClockById(events2[i][2])
            if(punchClock == []):
                continue
            course = self.dbMgr.getCourseById(punchClock[0])
            if(course == []):
                continue
            oneEvent = {
                "usrName": usrInfo[1],
                "usrImage": usrInfo[7],
                "usrId": usrInfo[8],
                "time1": time.asctime(time.localtime(events2[i][5])),
                "time2": time.asctime(time.localtime(events2[i][6])),
                "eventCode": events2[i][3],
                "eventStatus": eventStatus[str(events2[i][3])],
                "courseTitle": course[0],
                "courseName": course[1],
                "courseContent": course[2],
                "punchId": events2[i][2],
                "count": events2[i][4],
            }
            eventsRes2.append(oneEvent)
        return json.dumps({"res": "success", "events1": eventsRes1, "events2": eventsRes2})


