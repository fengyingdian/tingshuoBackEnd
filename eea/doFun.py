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

class doFun(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr

    #checkFileAudio
    def checkFileAudio(self, webData):
        mark1 = "Content-Type:"
        nPos1 = webData.find(mark1)
        nPos2 = 0
        if(nPos1 > 0):
            webData = webData[nPos1:]
            mark2 = "\r\n\r\n"
            nPos2 = webData.find(mark2)
            if(nPos2 > 0):
                return True
        return False

    #checkFileImage
    def checkFileImage(self, webData):
        mark1 = "Content-Type:"
        nPos1 = webData.find(mark1)
        nPos2 = 0
        if(nPos1 > 0):
            webData = webData[nPos1:]
            mark2 = "\r\n\r\n"
            nPos2 = webData.find(mark2)
            if(nPos2 > 0):
                return True
        return False

    #saveFileAudio
    def saveFileAudio(self, webData, path, file):
        mark1 = "Content-Type:"
        nPos1 = webData.find(mark1)
        nPos2 = 0
        if(nPos1 > 0):
            webData = webData[nPos1:]
            mark2 = "\r\n\r\n"
            nPos2 = webData.find(mark2)
            if(nPos2 > 0):
                utils.mkdir(path)
                with open(path + file, 'wb') as f:
                    f.write(webData[nPos2 + 4:])
                    f.close()
                    print("file: closed")
                    return True
        return False

    #saveFileImage
    def saveFileImage(self, webData, path, file):
        mark1 = "Content-Type:"
        nPos1 = webData.find(mark1)
        nPos2 = 0
        if(nPos1 > 0):
            webData = webData[nPos1:]
            mark2 = "\r\n\r\n"
            nPos2 = webData.find(mark2)
            utils.mkdir(path)
            with open(path + file, 'wb') as f:
                f.write(webData[nPos2 + 4:])
                f.close()
                print("file: closed")
                return True
        return False

    # getFullPunchInfo
    def getFullPunchInfo(self, punches):
        resData = []
        for index, value in enumerate(punches):
            courseId = value[0]
            courseInfo = self.dbMgr.getCourseById(courseId)
            if(courseInfo!=[]):
                resValue = courseInfo + value
                resData.append(resValue)
        return resData

    #getCourses
    def getCourses(self, data):
        resData = self.dbMgr.getCourses()
        if (resData == []):
            return resData
        resData2 = []
        for index, value in enumerate(resData):
            value = value + (0,)
            resData2.append(value)

        nowDate = datetime.datetime.now().strftime('%Y%m%d')
        res = self.dbMgr.getUsrGrade(int(data["usrId"]))
        if res != []:
            now = datetime.datetime.now()
            delta = datetime.timedelta(days=1)
            newDate = now + delta
            nowDate = newDate.strftime('%Y%m%d')
        courseData = []
        if data["usrId"] == "1":
            courseData = resData2
        else:
            for index, value in enumerate(resData2):
                if (value[1] <= nowDate):
                    courseData.append(value)
        return courseData

    #getClasses
    def getClasses(self, data):
        calssData = self.dbMgr.getClasses()
        if(calssData == []):
            return calssData
        resData = []
        for i in range(len(calssData)):
            classUsrs = self.dbMgr.getClassUsrIn(calssData[i][5])
            classUsrsNew = []
            for j in range(len(classUsrs)):
                temp1 = classUsrs[j]
                temp2 = self.dbMgr.getUsrInfo(temp1[0])
                if (temp2 != []):
                    classUsrsNew.append(temp1 + temp2)
            temp = {
                "classInfo": calssData[i],
                "classUsrs": classUsrsNew,
            }
            resData.append(temp)
        return resData

    #getCourse
    def getCourse(self, data):
        #get punch time
        punchTime = self.dbMgr.getPunchClocksByUsrId(int(data["usrId"]))
        #get comment time
        commentTime = self.dbMgr.getCommentsByUsrId(int(data["usrId"]))
        # get usr grade
        usrGrade = self.dbMgr.getUsrGrade(int(data["usrId"]))
        # get courseData
        courseData = self.dbMgr.getCourse(data["date"])
        if courseData == []:
            return json.dumps({"res": "fail", "courseData": [], "punchData": [], "usrGrade": usrGrade, "punchTime": punchTime, "commentTime": commentTime})
        punchData = self.dbMgr.getPunchClocksByCourseId(courseData[10])
        if punchData == []:
            return json.dumps({"res": "success", "courseData": courseData, "punchData": [], "usrGrade": usrGrade, "punchTime": punchTime, "commentTime": commentTime})
        classIds = []
        row = self.dbMgr.getClassBysName("VIPTrain", 1)
        classIds.append(row[5])
        row = self.dbMgr.getClassBysName("VIPTrain", 2)
        classIds.append(row[5])
        print("1102: classIds: ", classIds)
        punchDataNew = []
        if (data["class"] == "VIPTrain"):
            for index, value in enumerate(punchData):
                #print index, value
                usrClass = self.dbMgr.getUsrClass(value[1])
                if usrClass != []:
                    for index2, value2 in enumerate(usrClass):
                        temp = value
                        if (value2[1] == classIds[0] and value2[5] == 1 ):
                            tupleTemp = ("VIP", 1, value2[2])
                            temp = temp + tupleTemp
                            punchDataNew.append(temp)
                        elif (value2[1] == classIds[1] and value2[5] == 1):
                            tupleTemp = ("VIP", 2, value2[2])
                            temp = temp + tupleTemp
                            punchDataNew.append(temp)
        else:
            for index, value in enumerate(punchData):
                #print index, value
                usrClass = self.dbMgr.getUsrClass(value[1])
                temp = value
                if usrClass != []:
                    for index2, value2 in enumerate(usrClass):
                        if (value2[1] == classIds[0] and value2[5] == 1 ):
                            tupleTemp = ("VIP", 1, value2[2])
                            temp = temp + tupleTemp
                            break
                        elif (value2[1] == classIds[1] and value2[5] == 1 ):
                            tupleTemp = ("VIP", 2, value2[2])
                            temp = temp + tupleTemp
                            break
                        elif (value2[1] != classIds[0] and value2[1] != classIds[1]):
                            normalClass = self.dbMgr.getClassById(value2[1])
                            tupleTemp = (normalClass[1],normalClass[2],value2[2])
                            temp = temp + tupleTemp
                            break
                        else:
                            tupleTemp = ("None",0,0)
                            temp = temp + tupleTemp
                            break
                else:
                    tupleTemp = ("None", 0, 0)
                    temp = temp + tupleTemp
                punchDataNew.append(temp)
        resData = self.getPunchClocks(data, punchDataNew)
        return json.dumps({"res": "success", "courseData": courseData, "punchData": resData, "usrGrade": usrGrade, "punchTime": punchTime, "commentTime": commentTime})

    #getCourse2
    def getCourse2(self, data):
        # get usr grade
        usrGrade = self.dbMgr.getUsrGrade(int(data["usrId"]))
        # get courseData
        courseData = self.dbMgr.getCourse(data["date"])
        if courseData == []:
            return json.dumps({"res": "fail", "courseData": [], "punchData": [], "usrGrade": usrGrade})
        punchData = self.dbMgr.getPunchClocksByCourseId50(courseData[10])
        if punchData == []:
            return json.dumps({"res": "success", "courseData": courseData, "punchData": [], "usrGrade": usrGrade})
        classIds = []
        row = self.dbMgr.getClassBysName("VIPTrain", 1)
        classIds.append(row[5])
        row = self.dbMgr.getClassBysName("VIPTrain", 2)
        classIds.append(row[5])
        print("1102: classIds: ", classIds)
        punchDataNew = []
        if (data["class"] == "VIPTrain"):
            for index, value in enumerate(punchData):
                #print index, value
                usrClass = self.dbMgr.getUsrClass(value[1])
                if usrClass != []:
                    for index2, value2 in enumerate(usrClass):
                        temp = value
                        if (value2[1] == classIds[0] and value2[5] == 1 ):
                            tupleTemp = ("VIP", 1, value2[2])
                            temp = temp + tupleTemp
                            punchDataNew.append(temp)
                        elif (value2[1] == classIds[1] and value2[5] == 1):
                            tupleTemp = ("VIP", 2, value2[2])
                            temp = temp + tupleTemp
                            punchDataNew.append(temp)
        else:
            for index, value in enumerate(punchData):
                #print index, value
                usrClass = self.dbMgr.getUsrClass(value[1])
                temp = value
                if usrClass != []:
                    for index2, value2 in enumerate(usrClass):
                        if (value2[1] == classIds[0] and value2[5] == 1 ):
                            tupleTemp = ("VIP", 1, value2[2])
                            temp = temp + tupleTemp
                            break
                        elif (value2[1] == classIds[1] and value2[5] == 1 ):
                            tupleTemp = ("VIP", 2, value2[2])
                            temp = temp + tupleTemp
                            break
                        elif (value2[1] != classIds[0] and value2[1] != classIds[1]):
                            normalClass = self.dbMgr.getClassById(value2[1])
                            tupleTemp = (normalClass[1],normalClass[2],value2[2])
                            temp = temp + tupleTemp
                            break
                        else:
                            tupleTemp = ("None",0,0)
                            temp = temp + tupleTemp
                            break
                else:
                    tupleTemp = ("None", 0, 0)
                    temp = temp + tupleTemp
                punchDataNew.append(temp)
        resData = self.getPunchClocks(data, punchDataNew)
        return json.dumps({"res": "success", "courseData": courseData, "punchData": resData, "usrGrade": usrGrade})

    #getCourse3
    def getCourse3(self, data):
        # get courseData
        courseData = self.dbMgr.getCourse(data["date"])
        if courseData == []:
            return json.dumps({"res": "fail", "courseData": []})
        return json.dumps({"res": "success", "courseData": courseData})

    #getCourse
    def getCourse4(self, data):
        #get punch time
        punchTime = self.dbMgr.getPunchClocksByUsrId(int(data["usrId"]))
        #get comment time
        commentTime = self.dbMgr.getCommentsByUsrId(int(data["usrId"]))
        # get usr grade
        usrGrade = self.dbMgr.getUsrGrade(int(data["usrId"]))
        # get courseData
        courseData = self.dbMgr.getCourse(data["date"])
        if courseData == []:
            return json.dumps({"res": "fail", "courseData": [], "usrGrade": usrGrade, "punchTime": punchTime, "commentTime": commentTime})
        return json.dumps({"res": "success", "courseData": courseData, "usrGrade": usrGrade, "punchTime": punchTime, "commentTime": commentTime})

    #
    def getPunchClocks(self, data, punchData):
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
                        "punchId": value[5],
                        "usrId": value[1],
                        "practice": value[6],
                        "content": value[7],
                        "score": value[8],
                        "className": value[9],
                        "classType": value[10],
                        "classNumber": value[11],
                    }
                else:
                    usr = {
                        "name": "unknow",
                        "image": "../image/button/tourist.jpg",
                        "time": value[2],
                        "punchId": value[5],
                        "usrId": value[1],
                        "practice": value[6],
                        "content": value[7],
                        "score": value[8],
                        "className": value[9],
                        "classType": value[10],
                        "classNumber": value[11],
                    }
                usr["thumb"] = value[4]
                usrThumb = self.dbMgr.getPunchThumb(value[5], int(data["usrId"]))
                if (usrThumb != None):
                    if (usrThumb[3] == 1):
                        usr["hasThumb"] = True
                    else:
                        usr["hasThumb"] = False
                else:
                    usr["hasThumb"] = False

                thumbs = self.dbMgr.getPunchThumbs(value[5])
                usr["thumbUp"] = len(thumbs)
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
                        "date": data["date"],
                        "punchId": str(value[5]),
                        "usrId": data["usrId"]
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
                        "punchId": value[0],
                        "usrId": value[1],
                        "contentType": value[3],
                        "content": value[4],
                        "commentId": value[6],
                        "toUsrId": value[7],
                    }
                else:
                    usr = {
                        "index": index,
                        "name": "unknow",
                        "image": "../image/button/tourist.jpg",
                        "time": value[2],
                        "punchId": value[0],
                        "usrId": value[1],
                        "contentType": value[3],
                        "content": value[4],
                        "commentId": value[6],
                        "toUsrId": value[7],
                    }
                if(usr["toUsrId"]!=0):
                    toUsrInfo = self.dbMgr.getUsrInfo(usr["toUsrId"])
                    if(toUsrInfo!=[]):
                        usr["toUsrName"] = toUsrInfo[1],
                else:
                    usr["toUsrName"] = "host",

                usrThumb = self.dbMgr.getCommentThumb(value[6], int(data["usrId"]))
                if(usrThumb != None):
                    if(usrThumb[3] == 1):
                        usr["hasThumb"] = True
                    else:
                        usr["hasThumb"] = False
                else:
                    usr["hasThumb"] = False

                thumbs = self.dbMgr.getCommentThumbs(value[6])
                usr["thumb"] = len(thumbs)

                if(usr["contentType"]==2):
                    usr["contentText"] = usr["content"]
                    usr["content"] = path + str(usr["commentId"]) + ".m4a"
                elif (usr["contentType"] == 3):
                    usr["contentText"] = usr["content"]
                    usr["content"] = path + str(usr["commentId"]) + ".mp3"
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

    #
    def dealNewComment(self, data):
        #save new formId
        userOpenId = self.dbMgr.getUsrOpenId(int(data["usrId"]))
        self.dbMgr.insertFormId(userOpenId, data["formId"])

        #send templateMessage
        openId = ""
        if (data.has_key("toUsrId")):
            openId = self.dbMgr.getUsrOpenId(int(data["toUsrId"]))
            data["punchHostId"] = data["toUsrId"]
        else:
            openId = self.dbMgr.getUsrOpenId(int(data["punchHostId"]))
        formId = self.dbMgr.getValidFormId(openId)

        #send  templateMessage
        if(data["punchHostId"]!=data["usrId"] and type(formId)!=type(None)):
            url = "pages/recordShow/recordShow?" + "date=" + data["date"] + "&punchId=" + str(data["punchId"])
            url = url + "&classType=" + data["classType"] + "&loadType=" + data["loadType"]
            print("1300: url", url)
            course = self.dbMgr.getCourse(data["date"])
            data["punchContent"] = course[2]
            usrInfo = self.dbMgr.getUsrInfo(int(data["usrId"]))
            if(usrInfo!=[]):
                data["commmentName"] = usrInfo[1]
                if(data["contentType"] == 2):
                    data["content"] = u"语音"
                wx = wxServer()
                resText = wx.postMessageToUser(openId, formId, url, data["time"],
                                               u"小伙伴给你回复啦，快去看看吧~", "default", data["punchContent"], data["content"],
                                               data["commmentName"])
        #get comment data
        commentData = self.dbMgr.getCommentsByPunchId(int(data["punchId"]))
        print ("1300: commentData: ", commentData)
        if commentData != []:
            resData = self.getComments(data, commentData)
            return json.dumps({"res": "success", "commentData": resData})
        else:
            return json.dumps({"res": "success", "commentData": []})

    #
    def postPunchClockNotification(self):
        usrs = self.dbMgr.getUsrs()
        if(usrs == []):
            return json.dumps({"res": "success", "usrInfo": usrs})
        url = "pages/index/index"
        wx = wxServer()
        for index, value in enumerate(usrs):
            time.sleep(10)
            usrId = value[8]
            punches = self.dbMgr.getPunchClocksByUsrId(usrId)
            notice = str()
            if (punches == []):
                notice = u"您还没有打卡~不要让等你的小伙伴失望哦~"
            else:
                notice = u"您已打卡"
                notice = notice + str(punches.__len__())
                notice = notice + u"次，继续加油哦~"
            openId = value[0]
            formId = self.dbMgr.getValidFormId(openId)
            resText = wx.postNotificationToUser(openId, formId, url, notice)
            print("template:", resText)
        return json.dumps({"res": "success", "data": 2})

    #
    def postVersionChangeToUsr(self):
        usrs = self.dbMgr.getUsrs()
        if(usrs == []):
            return json.dumps({"res": "success", "usrInfo": usrs})
        url = "pages/index/index"
        wx = wxServer()
        for index, value in enumerate(usrs):
            time.sleep(10)
            usrId = value[8]
            punches = self.dbMgr.getPunchClocksByUsrId(usrId)
            notice = str()
            if (punches == []):
                notice = u"您还没有打卡~不要让等你的小伙伴失望哦~"
            else:
                notice = u"您已打卡"
                notice = notice + str(punches.__len__())
                notice = notice + u"次，继续加油哦~"
            openId = value[0]
            formId = self.dbMgr.getValidFormId(openId)
            resText = wx.postVersionChangeToUser(openId, formId, url, notice)
            print("template:", resText)
        return json.dumps({"res": "success", "data": 2})

    #
    def ranking(self):
        usrs = self.dbMgr.getUsrs()
        if(usrs == []):
            return json.dumps({"res": "success", "usrInfo": usrs})

        rank1 = []
        rank2 = []
        for i in range(len(usrs)):
            temp1 = usrs[i]
            punchs = self.dbMgr.getPunchClocksByUsrId(temp1[8])
            comments = self.dbMgr.getCommentsByUsrId(temp1[8])
            temp2 = (len(punchs),len(comments)) + temp1
            rank1.append(temp2)
            temp3 = (len(comments),) + temp1
            rank2.append(temp3)

        rank1 = self.bubble_sort(rank1)
        rank2 = self.bubble_sort(rank2)

        ticks = time.time()
        date = time.strftime("%Y-%m-%d", time.localtime())
        for i in range(len(rank1)):
            if(i > 49):
                break
            res = self.dbMgr.insertPunchRanking(date, rank1[i][10], rank1[i][0], rank1[i][1], i+1, ticks)
            #res1.append(res)

        for i in range(len(rank2)):
            if (i > 49):
                break
            res = self.dbMgr.insertCommentRanking(date, rank2[i][9], rank2[i][0], i + 1, ticks)
            #res2.append(res)

        return json.dumps({"res": "success", "data1": rank1, "data2": rank2})

    #
    def bubble_sort(self, lists):
        count = len(lists)
        for i in range(0, count):
            for j in range(i + 1, count):
                if lists[i][0] < lists[j][0]:
                    lists[i], lists[j] = lists[j], lists[i]
        return lists