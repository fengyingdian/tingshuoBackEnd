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

class doFun1(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr

    #getCourses
    def getCourses(self, data, courseId, course, classInfo):
        resData = {
            "courseData": [],
            "punchData": [],
        }
        # get courseData
        courseData = self.dbMgr.getCourseById(courseId)
        if courseData == []:
            return resData
        tempCourse = courseData + course
        resData["courseData"] = tempCourse

        punchData = self.dbMgr.getPunchClocksByCourseId(courseId)
        if punchData == []:
            return resData
        punchDataNew = []
        for index, value in enumerate(punchData):
            usrClass = self.dbMgr.getUsrClassInfo(value[1], int(data["classId"]))
            if usrClass != []:
                if(usrClass[5] == 1):
                    tupleTemp = (classInfo[1], classInfo[2], usrClass[2])
                    temp = value + tupleTemp
                    punchDataNew.append(temp)
        resPunchData = self.getPunchClocks(data, courseData, punchDataNew)
        resData["punchData"] = resPunchData
        return resData

    #
    def getPunchClocks(self, data, courseData, punchData):
        if punchData != []:
            resData = []
            for index, value in enumerate(punchData):
                #print("punch: ", index, value, len(value))
                if(value[1] == -1):
                    continue
                usrInfo = self.dbMgr.getUsrInfo(value[1])
                usr = {}
                if(usrInfo != []):
                    usr = {
                        "name": usrInfo[1],
                        "image": usrInfo[7],
                        "time": value[2],
                        "thumb": value[4],
                        "punchId": value[5],
                        "usrId": value[1],
                        "className": value[7],
                        "classType": value[8],
                        "classNumber": value[9],
                    }
                else:
                    usr = {
                        "name": "unknow",
                        "image": "",
                        "time": value[2],
                        "thumb": value[4],
                        "punchId": value[5],
                        "usrId": value[1],
                        "className": value[7],
                        "classType": value[8],
                        "classNumber": value[9],
                    }
                #get usr grade
                resGrade = self.dbMgr.getUsrGrade(value[1])
                if resGrade != []:
                    usr["role"] = resGrade[1]
                else:
                    usr["role"] = "None"
                #get punchs comments
                if (type(value[5]) != type(None)):
                    commentData = self.dbMgr.getCommentsByPunchId(value[5])
                    tempData = {
                        "date": courseData[1],
                        "punchId": str(value[5]),
                    }
                    comments = self.getComments(tempData, commentData)
                    usr["comments"] = comments
                else:
                    usr["comments"] = []
                resData.append(usr)
            return resData
        else:
            return []

    #
    def getComments(self, data, commentData):
        if commentData == [] or type(data) == type(None):
            return "None"
        path = "https://www.abceea.com/static/class/" + data["date"] + "/" + data["punchId"] + "/"
        #print("path: ", path)
        resData = []
        for index, value in enumerate(commentData):
            #print("id: ", value[1])
            if(value[1] > 0):
                usrInfo = self.dbMgr.getUsrInfo(value[1])
                usr = {}
                if(usrInfo!=[]):
                    usr = {
                        "index": index,
                        "name": usrInfo[1],
                        "image": usrInfo[7],
                        "time": value[2],
                        "thumb": value[5],
                        "punchId": value[0],
                        "usrId": value[1],
                        "contentType": value[3],
                        "content": value[4],
                        "commentId": value[6],
                    }
                else:
                    usr = {
                        "index": index,
                        "name": "unknow",
                        "image": "",
                        "time": value[2],
                        "thumb": value[5],
                        "punchId": value[0],
                        "usrId": value[1],
                        "contentType": value[3],
                        "content": value[4],
                        "commentId": value[6],
                    }
                if(usr["contentType"]==2):
                    usr["content"] = path + str(usr["commentId"]) + ".m4a"
                # get usr grade
                resGrade = self.dbMgr.getUsrGrade(value[1])
                if resGrade != []:
                    usr["role"] = resGrade[1]
                else:
                    usr["role"] = "None"
                #print("res: ", res)
            resData.append(usr)
        if resData != []:
            return resData
        else:
            return "None"