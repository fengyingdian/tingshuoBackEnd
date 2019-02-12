# -*- coding: utf-8 -*-
# filename: do.py

import requests

import json

from databaseManage import databaseManage

import doPost

import doGet

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

class do(object):
    #
    def __init__(self):
        self.dbMgr = databaseManage()
        reload(doPost)
        self.post = doPost.doPost(self.dbMgr)
        reload(doGet)
        self.get = doGet.doGet(self.dbMgr)

    def doPost(self, data, webData):
        try:
            return self.post.do(data, webData)
        except Exception, Argument:
            print("request wx server failed:", data, Argument)
            return json.dumps({"res": "error: " + str(Argument)})

    def doGet(self, data):
        #
        try:
            return self.get.do(data)
        except Exception, Argument:
            print("request wx server failed:", data, Argument)
            return json.dumps({"res": "error: " + str(Argument)})

#test
if __name__ == '__main__':
    do = do()
