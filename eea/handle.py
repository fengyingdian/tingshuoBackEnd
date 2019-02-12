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
            web.header('Content-Type', 'application/json; charset=utf-8')
            data = web.input()
            if len(data) == 0:
                return "Welcome! this is EEA!"
            print ("Handle get data is ", data)
            reload(do)
            woker = do.do()
            return woker.doGet(data)
        except Exception, Argument:
            return Argument

    def POST(self):
        try:
            web.header('Content-Type', 'application/json; charset=utf-8')
            webData = web.data()
            data = web.input()
            if len(data) | len(webData) == 0:
                return "Welcome! this is EEA!"

            print ("Handle get data is ", data)# 后台打日志
            print ("Handle get webdata is ", webData)  # 后台打日志
            reload(do)
            woker = do.do()
            return woker.doPost(data, webData)
        except Exception, Argument:
            return Argument
