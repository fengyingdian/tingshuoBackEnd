# -*- coding: utf-8 -*-
# filename: handle.py

#
try:
  import cookielib
except:
  import http.cookiejar as cookielib

import web
import do
import threading
import utils

class Handle(object):
    def GET(self):
        try:
            data = web.input()
            if len(data) == 0:
                return "Welcome! this is EEA!"

            print ("Handle get data is ", data),# 后台打日志
            print threading.currentThread()
            reload(do)
            woker = do.do()
            return woker.doGet(data)
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            webData = web.data()
            data = web.input()
            if len(data) | len(webData) == 0:
                return "Welcome! this is EEA!"

            print ("Handle get data is ", data)# 后台打日志
            #print ("Handle get webdata is ", webData)  # 后台打日志

            reload(do)
            woker = do.do()
            return woker.doPost(data, webData)
        except Exception, Argument:
            return Argument
