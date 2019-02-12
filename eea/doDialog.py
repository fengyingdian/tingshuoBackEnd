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

from wxServer import wxServer

class doDialog(object):
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr

    # 上传课件
    def do2000(self, data):
        localTime = time.time()
        res = self.dbMgr.addDialog(data["title"],data["name"],int(localTime))
        res = self.dbMgr.getDialog(data["title"],data["name"])
        dialogId = res[3]
        count = int(data["count"])
        for i in range(count):
            self.dbMgr.addDialogContent(dialogId, data["role" + str(i+1)], data["content" + str(i+1)], data["translate" + str(i+1)], data["audioSrc" + str(i+1)])
        return json.dumps({"res": "success"})

    # 获取课件
    def do2001(self, data):
        res = self.dbMgr.getDialog(data["title"],data["name"])
        if(res == []):
            return json.dumps({"res": "not existed"})
        contents = self.dbMgr.getDialogContentByCourseId(res[3])
        return json.dumps({"res": "success", "contents": contents, "title": res[0], "name": res[1]})