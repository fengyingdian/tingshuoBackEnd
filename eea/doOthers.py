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

import doFun1
import doFun3

from wxServer import wxServer

class doOthers(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr
        reload(doFun)
        self.doFun = doFun.doFun(dbMgr)
        reload(doFun1)
        self.doFun1 = doFun1.doFun1(dbMgr)
        reload(doFun3)
        self.doFun3 = doFun3.doFun3(dbMgr)

    def do0000(self, data):
        #每日一句
        data = self.doFun.getCourses(data)
        #美式音标基础
        data1 = [
            {"name": "元音I", "id": 1},
            {"name": "元音i", "id": 2},
            {"name": "元音e", "id": 3},
        ]
        #美式音标提高
        data2 = [
            {"name": "连读", "id": 1},
            {"name": "吞音", "id": 2},
            {"name": "爆破", "id": 3},
        ]
        course = [
            {"title": "每日一句", "data": data},
            {"title": "美式音标基础", "data": data1},
            {"title": "美式音标提高", "data": data2},
        ]
        return json.dumps({"res": "success", "course": course})

    def do0001(self, data):
        #顶部广告栏
        topShows = [{
            "name": '每日英语',
            "info": "由EEA全体老师共同打造的以详细讲解英美影视剧经典片段为主，每天一更的经典课程，累计参与打卡人次已经超过10w，快来加入我们吧！",
            "image": "https://www.abceea.com/static/others/indexShowTop1.jpg"
        }]
        #每日一句
        everyDayCourse = self.doFun.getCourses(data)
        #所有的打卡
        punches = self.dbMgr.getPunchClocksByUsrId(int(data["usrId"]))
        fullPunchInfo = self.doFun.getFullPunchInfo(punches)
        #所有的点评
        #comments = self.dbMgr.getCommentsByUsrId(int(data["usrId"]))
        #其他课件
        #------
        #titles
        courseTitles = [
            {"title": "每日一句",
             "subTitles": [
                 {"title": "课程列表", "calendar": False, "data": everyDayCourse},
                 {"title": "我的打卡", "calendar": True, "data": [], "punches": fullPunchInfo},
                 {"title": "我的单词", "calendar": False, "data": []}]},
            {"title": "听写一百篇",
             "subTitles": [
                 {"title": "课程列表", "calendar": False, "data": []},
                 {"title": "我的打卡", "calendar": False, "data": []},
                 {"title": "我的单词", "calendar": False, "data": []}]},
            {"title": "美式音标基础",
             "subTitles": [
                 {"title": "课程列表", "calendar": False, "data": []},
                 {"title": "我的打卡", "calendar": False, "data": []},
                 {"title": "我的单词", "calendar": False, "data": []}]},
            {"title": "美式音标提高",
             "subTitles": [
                 {"title": "课程列表", "calendar": False, "data": []},
                 {"title": "我的打卡", "calendar": False, "data": []},
                 {"title": "我的单词", "calendar": False, "data": []}]},
            {"title": "我的课件",
             "subTitles": [
                 {"title": "课程列表", "calendar": False, "data": []},
                 {"title": "我的打卡", "calendar": False, "data": []},
                 {"title": "我的单词", "calendar": False, "data": []}]}]
        return json.dumps({"res": "success", "courseTitles": courseTitles, "topShows": topShows})

    def do0002(self, data):
        topShows = []
        calsses = self.doFun.getClasses(data)
        return json.dumps({"res": "success", "calsses": calsses, "topShows": topShows})

    def do0003(self, data):
        suggetValue = {
            "professor": 5,
            "teacher": 5,
            "monitor": 2,
            "monitorAssistant": 2,
            "secretary": 1,
            "editor": 1,
            "teacherAssistant": 1,
            "backup": 1,
            "supervisor": 5,
        }
        usrs = self.dbMgr.getPunchRanking(data["date"])
        if(usrs == []):
            return json.dumps({"res": "fail"})
        resData = []
        for i in range(len(usrs)):
            temp1 = usrs[i]
            temp2 = self.dbMgr.getUsrInfo(temp1[1])
            if (temp2 != []):
                temp3 = self.dbMgr.getUsrGrade(temp1[1])
                if(temp3 == []):
                    resData.append(temp1+temp2+(1,))
                else:
                    resData.append(temp1 + temp2 + (suggetValue[temp3[1]],))

        return json.dumps({"res": "success", "data": resData})

    def do0004(self, data):
        usrs = self.dbMgr.getcommentRanking(data["date"])
        if(usrs == []):
            return json.dumps({"res": "fail"})
        resData = []
        for i in range(len(usrs)):
            temp1 = usrs[i]
            temp2 = self.dbMgr.getUsrInfo(temp1[1])
            if (temp2 != []):
                resData.append(temp1+temp2)
        return json.dumps({"res": "success", "data": resData})

    def do0005(self, data):
        usrs1 = self.dbMgr.getPunchRanking(data["date"])
        if(usrs1 == []):
            return json.dumps({"res": "fail"})
        resData1 = []
        for i in range(len(usrs1)):
            temp1 = usrs1[i]
            temp2 = self.dbMgr.getUsrInfo(temp1[1])
            if(temp2!=[]):
                resData1.append(temp1+temp2)
        usrs2 = self.dbMgr.getcommentRanking(data["date"])
        if(usrs2 == []):
            return json.dumps({"res": "fail"})
        resData2 = []
        for i in range(len(usrs2)):
            temp1 = usrs2[i]
            temp2 = self.dbMgr.getUsrInfo(temp1[1])
            if (temp2 != []):
                resData2.append(temp1+temp2)
        return json.dumps({"res": "success", "punchRank": resData1, "commentRank": resData2})

    def do1000(self, data):
        webUrl = "https://api.weixin.qq.com/sns/jscode2session?appid=wxc14f34923223ee96&secret=02e6e0b9a69784477e392ab9df9f64e4&js_code=" + \
                 data["code"] + "&grant_type=authorization_code"
        resData = json.loads(requests.session().get(url=webUrl).text)
        print(resData)
        print(resData["openid"])
        if (resData["openid"]):
            resData["nickName"] = "tourist"
            resData["gender"] = "0"
            resData["city"] = "unknow"
            resData["province"] = "unknow"
            resData["country"] = "unknow"
            resData["language"] = "en"
            resData["imageSrc"] = "../image/button/tourist.jpg"
            miniId, resInfo = self.dbMgr.addUser(resData["openid"], resData["nickName"], int(resData["gender"]),
                                                 resData["city"], resData["province"], resData["country"],
                                                 resData["language"], resData["imageSrc"])
            userInfo = {
                "nickName": resInfo[1],
                "gender": resInfo[2],
                "city": resInfo[3],
                "province": resInfo[4],
                "country": resInfo[5],
                "language": resInfo[6],
                "imageSrc": resInfo[7],
            }
            return json.dumps({"res": "success", "miniId": miniId, "userInfo": userInfo})
        else:
            return json.dumps({"res": "failed"})

    def do1001(self, data):
        if (data["id"]):
            print("handle:", data["imageSrc"])
            return json.dumps({"res": self.dbMgr.modifyUser(int(data["id"]), data["nickName"], int(data["gender"]),
                                                            data["city"], data["province"], data["country"],
                                                            data["language"], data["imageSrc"])})
        else:
            return json.dumps({"res": "false", "miniId": 0})

    def do1002(self, data):
        webUrl = "https://api.weixin.qq.com/sns/jscode2session?appid=wxc14f34923223ee96&secret=02e6e0b9a69784477e392ab9df9f64e4&js_code=" + \
                 data["code"] + "&grant_type=authorization_code"
        resData = json.loads(requests.session().get(url=webUrl).text)
        return json.dumps({"res": resData})
        print(resData["openid"])
        if (resData["openid"]):
            miniId, resInfo = self.dbMgr.relogUser(resData["openid"], data["nickName"], int(data["gender"]),
                                                   data["city"], data["province"], data["country"], data["language"],
                                                   data["imageSrc"])
            print ("miniId, resInfo: ", miniId, resInfo)
            userInfo = {
                "nickName": resInfo[1],
                "gender": resInfo[2],
                "city": resInfo[3],
                "province": resInfo[4],
                "country": resInfo[5],
                "language": resInfo[6],
                "imageSrc": resInfo[7],
            }
            return json.dumps({"res": "success", "miniId": miniId, "userInfo": userInfo})
        else:
            return json.dumps({"res": "failed"})

    def do1003(self, data):
        userInfo = self.dbMgr.getUsrInfo(int(data["usrId"]))
        if (userInfo != []):
            return json.dumps({"res": "success", "userInfo": userInfo})
        else:
            return json.dumps({"res": "not existed"})

    def do1400(self, data):
        verifyCode = {
            "professor": "5675",
            "teacher": "3452",
            "monitor": "2346",
            "monitorAssistant": "789869",
            "secretary": "67657",
            "editor": "5645645",
            "teacherAssistant": "234234"
        }
        if (verifyCode[data["role"]] != data["code"]):
            if (data["code"] == "907845"):
                data["role"] = "supervisor"
            elif (data["code"] == "014654"):
                data["role"] = "backup"
            elif (data["code"] == "8200"):
                return self.doFun.ranking()
            elif (data["code"] == "9011"):
                return self.doFun.postPunchClockNotification()
            elif (data["code"] == "9033"):
                return self.doFun.postVersionChangeToUsr()
            elif (data["code"] == "9022"):
                return self.dbMgr.deleteFormId()
            elif (data["code"] == "1022"):
                result = self.doFun3.getScoreShengXi("", "Hello, This is a test.")
                return json.dumps({"res": result})
            else:
                return json.dumps({"res": "fail"})
        print (data["role"])
        res = self.dbMgr.addUsrGrade(int(data["usrId"]), data["role"])
        return json.dumps({"res": "success"})

    def do1401(self, data):
        res = self.dbMgr.getUsrGrade(int(data["usrId"]))
        if (res != []):
            return json.dumps({"res": "success", "role": res[1]})
        else:
            return json.dumps({"res": "fail"})

    def do1500(self, data):
        localtime = time.asctime(time.localtime(time.time()))
        data["time"] = localtime
        res = self.dbMgr.addClass(data["name"], data["sName"], int(data["classType"]), int(data["maxCount"]), data["info"],data["coverSrc"],int(data["admittance"]),int(data["punchLimit"]),data["time"],int(data["usrId"]))
        return json.dumps({"res": "success", "data": res})

    def do1501(self, data):
        usrClass = self.dbMgr.getUsrClass(int(data["usrId"]))
        classData = []
        if (usrClass != []):
            for index, value in enumerate(usrClass):
                print index, value
                oneClass = self.dbMgr.getClassById(value[1])
                print("oneClass:", oneClass)
                classData.append(oneClass)
        usrGrade = self.dbMgr.getUsrGrade(int(data["usrId"]))
        return json.dumps({"res": "success", "classData": classData, "grade": usrGrade})

    def do1502(self, data):
        vipClass = self.dbMgr.getClass("VIP集训营", "VIPTrain", int(data["classType"]))
        print("vipClass:", vipClass)
        if (vipClass == []):
            return json.dumps({"res": "fail"})
        res = self.dbMgr.addUsrClass(int(data["usrId"]), vipClass[5], level=0, status=1)
        return json.dumps({"res": res})

    def do1503(self, data):
        usrClassInfo = self.dbMgr.getUsrClassInfo(int(data["usrId"]),int(data["classId"]))
        if (usrClassInfo == []):
            return json.dumps({"res": "fail"})
        return json.dumps({"res": "success", "usrClassInfo": usrClassInfo})

    def do1504(self, data):
        classInfo = self.dbMgr.getClassById(int(data["classId"]))
        if(classInfo == []):
            return json.dumps({"res": "fail"})

        usrClass = self.dbMgr.getClassUsrIn(classInfo[5])
        return json.dumps({"res": "success", "classInfo": classInfo, "usrClass": usrClass})

    def do1505(self, data):
        insertTime = int(time.time())
        count = int(data["count"])
        classId = int(data["classId"])
        usrId = int(data["usrId"])
        postDate = data["postDate"]
        resSatus = "success"
        for i in range(count):
            res = self.dbMgr.addClassCourse(classId, int(data["courseId"+str(i+1)]), usrId, postDate, insertTime)
            if(res == "existed"):
                resSatus = "existed"
        return json.dumps({"res": resSatus})

    def do1506(self, data):
        classInfo = self.dbMgr.getClassById(int(data["classId"]))
        if(classInfo == []):
            return json.dumps({"res": "fail"})

        if (data.has_key("loadType")):
            if (int(data["loadType"]) == 2):
                tempUsr = self.dbMgr.getUsrClassInfo(int(data["usrId"]), classInfo[5])
                if (tempUsr == []):
                    if (classInfo[7] == 0):
                        res = self.dbMgr.addUsrClass(int(data["usrId"]), classInfo[5], level=0, status=1)
                    else:
                        return json.dumps({"res": "no"})
                else:
                    if (classInfo[7] == 0):
                        if (tempUsr[5] == 0):
                            return json.dumps({"res": "tickOff"})
                        elif (tempUsr[5] == 3):
                            self.dbMgr.modifyUsrClass(tempUsr[0], tempUsr[1], tempUsr[2], 0, 1)
                    else:
                        if (tempUsr[5] != 1):
                            return json.dumps({"res": "no"})

        classUsrs = self.dbMgr.getClassUsr(classInfo[5])
        classUsrsNew = []
        for i in range(len(classUsrs)):
            temp1 = classUsrs[i]
            temp2 = self.dbMgr.getUsrInfo(temp1[0])
            if (temp2 != []):
                classUsrsNew.append(temp1 + temp2)

        usrInfo = self.dbMgr.getUsrClassInfo(int(data["usrId"]), int(data["classId"]))

        classCourse = self.dbMgr.getClassCourseInfo(int(data["classId"]))
        if(classCourse == []):
            return json.dumps({"res": "success", "classInfo": classInfo, "classUsrs": classUsrsNew,
                               "usrInfo": usrInfo, "classCourse": classCourse, "courseDatas": []})

        courseDatas = []
        for i in range(len(classCourse)):
            courseId = classCourse[i][1]
            oneCoursePunch = self.doFun1.getCourses(data, courseId, classCourse[i], classInfo)
            courseDatas.append(oneCoursePunch)
        return json.dumps({"res": "success", "classInfo": classInfo, "classUsrs": classUsrsNew,
                               "usrInfo": usrInfo, "classCourse": classCourse, "courseDatas": courseDatas})

    def do1507(self, data):
        classInfo = self.dbMgr.getClassById(int(data["classId"]))
        if (classInfo == []):
            return json.dumps({"res": "deleted"})
        res = self.dbMgr.addUsrClass(int(data["usrId"]), classInfo[5], level=0, status=int(data["status"]))
        if(res == "existed"):
            usrInfo = self.dbMgr.getUsrClassInfo(int(data["usrId"]), int(data["classId"]))
            if (usrInfo == []):
                return json.dumps({"res": "missed"})
            if (usrInfo[5] == 0):
                return json.dumps({"res": "tickOff"})
            if (usrInfo[5] != 2):
                resModify = self.dbMgr.modifyUsrClass(usrInfo[0], usrInfo[1], usrInfo[2], 0, int(data["status"]))
                if (resModify != "success"):
                    return json.dumps({"res": "fail"})
                else:
                    return json.dumps({"res": resModify})
        return json.dumps({"res": res})

    def do1508(self, data):
        classInfo = self.dbMgr.getClassById(int(data["classId"]))
        if (classInfo == []):
            return json.dumps({"res": "deleted"})

        usrInfo = self.dbMgr.getUsrClassInfo(int(data["classUsrId"]), int(data["classId"]))
        if (usrInfo == []):
            return json.dumps({"res": "missed"})

        res = self.dbMgr.modifyUsrClass(usrInfo[0], usrInfo[1], usrInfo[2], int(data["level"]), int(data["status"]))
        if(res != "success"):
            return json.dumps({"res": "fail"})

        classUsrs = self.dbMgr.getClassUsr(int(data["classId"]))
        classUsrsNew = []
        for i in range(len(classUsrs)):
            temp1 = classUsrs[i]
            temp2 = self.dbMgr.getUsrInfo(temp1[0])
            if (temp2 != []):
                classUsrsNew.append(temp1 + temp2)
        return json.dumps({"res": "success", "classUsrs": classUsrsNew})

    def do1509(self, data):
        res = self.dbMgr.deleteClassCourseById(int(data["id"]))
        return json.dumps({"res": res})

    def do1510(self, data):
        res1 = self.dbMgr.deleteClassById(int(data["classId"]))
        if(res1 == "not existed"):
            return json.dumps({"res": "deleted"})
        res2 = self.dbMgr.deleteClassUsrByClassId(int(data["classId"]))
        return json.dumps({"res": res2})

    def do8001(self, data):
        punches = self.dbMgr.getPunchClocksByUsrId(int(data["usrId"]))
        comments = self.dbMgr.getCommentsByUsrId(int(data["usrId"]))
        return json.dumps({"res": "success", "punchTime": punches, "commentTime": comments})

    def do9001(self, data):
        webUrl = "https://api.weixin.qq.com/sns/jscode2session?appid=wxc14f34923223ee96&secret=647411124a76822848e5d7303d19f4a4&js_code=" + \
                 data["code"] + "&grant_type=authorization_code"
        resData = json.loads(requests.session().get(url=webUrl).text)
        print("9001: resData ", resData)
        print("9001: data ", data)
        if (resData["openid"] and resData["session_key"]):
            pc = WXBizDataCrypt("wxc14f34923223ee96", resData["session_key"])
            res = pc.decrypt(data["encryptedData"], data["iv"])
            print("9001: res ", res)
            return json.dumps({"res": "success", "data": res})
        else:
            return json.dumps({"res": "fail"})

    def do9002(self, data):
        openId = self.dbMgr.getUsrOpenId(int(data["usrId"]))
        print("9002: insertFormId ", self.dbMgr.insertFormId(openId, data["formId"]))