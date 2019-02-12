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

import urllib2
import time
import urllib
import json
import hashlib
import base64

class doFun3(object):
    #
    def __init__(self, dbMgr):
        self.dbMgr = dbMgr

    def getScore(self, voiceContent, text):
        f = open("./temp/test.wav", 'rb')
        file_content = f.read()
        base64_audio = base64.b64encode(file_content)
        body = urllib.urlencode({'audio': base64_audio, 'text': text})

        url = 'http://api.xfyun.cn/v1/service/v1/ise'
        api_key = 'c1dd26c46a55ed784d5edd5303c29428'
        param = {"aue": "raw", "result_level": "entirety", "language": "en_us", "category": "read_sentence"}

        x_appid = '5b712d8a'
        x_param = base64.b64encode(json.dumps(param).replace(' ', ''))
        x_time = int(int(round(time.time() * 1000)) / 1000)
        x_checksum = hashlib.md5(api_key + str(x_time) + x_param).hexdigest()
        x_header = {'X-Appid': x_appid,
                    'X-CurTime': x_time,
                    'X-Param': x_param,
                    'X-CheckSum': x_checksum}
        req = urllib2.Request(url, body, x_header)
        result = urllib2.urlopen(req)
        result = result.read()
        return result

    def getScoreShengXi(self, voiceContent, text):
        api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWVzdCIsInN1YiI6InNwZWVjaHhfbWRkIiwiU2lnbmVkQnkiOiJqc3pob25nIiwibkNsaWVudElEIjoxNTM0MzE1MjA1LCJFbmdsaXNoTGV2ZWwiOjMsIm5NYXhDb25jdXJyZW50VXNlciI6MCwiUHVibGlzaGVyTmFtZSI6ImJlaWRhdGluZ3NodW8iLCJGZWVkQmFja1R5cGUiOjYsImlzcyI6ImF1dGgwIiwibkdCX1VTIjowLCJleHAiOjE1Mzk1MzI4MDV9.f84FB5dff5C-4DYOJjlbc-8_AknQEV31xxdyEZ6rAAE"
        url = "https://t02.io.speechx.cn:8443/MDD_Server/mdd_v18"
        headers = {'Authorization': 'Bearer {0}'.format(api_token)}
        audio_path = "./temp/test.wav"
        files = dict(myWavfile=open(audio_path, 'rb'))
        data = dict(word_name=text, myWavefile=audio_path)
        response = requests.post(url, files=files, data=data, headers=headers)
        response_json = response.json()
        with open("./static/testData.txt", 'wb') as f:
            f.write(response.text)
            f.close()

        return response_json

    def getScoreShengXi2(self, filePath, text):
        api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWVzdCIsInN1YiI6InNwZWVjaHhfbWRkIiwiU2lnbmVkQnkiOiJqc3pob25nIiwibkNsaWVudElEIjoxNTM0MzE1MjA1LCJFbmdsaXNoTGV2ZWwiOjMsIm5NYXhDb25jdXJyZW50VXNlciI6MCwiUHVibGlzaGVyTmFtZSI6ImJlaWRhdGluZ3NodW8iLCJGZWVkQmFja1R5cGUiOjYsImlzcyI6ImF1dGgwIiwibkdCX1VTIjowLCJleHAiOjE1Mzk1MzI4MDV9.f84FB5dff5C-4DYOJjlbc-8_AknQEV31xxdyEZ6rAAE"
        url = "https://t02.io.speechx.cn:8443/MDD_Server/mdd_v18"
        headers = {'Authorization': 'Bearer {0}'.format(api_token)}
        files = dict(myWavfile=open(filePath, 'rb'))
        data = dict(word_name=text, myWavefile=filePath, user_id="tingshouPKU")
        response = requests.post(url, files=files, data=data, headers=headers)
        response_json = response.json()
        return response_json

    def getScoreShengXi3(self, file, filePath, text):
        api_token = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJhdWQiOiJndWVzdCIsInN1YiI6InNwZWVjaHhfbWRkIiwiU2lnbmVkQnkiOiJqc3pob25nIiwibkNsaWVudElEIjoxNTM0MzE1MjA1LCJFbmdsaXNoTGV2ZWwiOjMsIm5NYXhDb25jdXJyZW50VXNlciI6MCwiUHVibGlzaGVyTmFtZSI6ImJlaWRhdGluZ3NodW8iLCJGZWVkQmFja1R5cGUiOjYsImlzcyI6ImF1dGgwIiwibkdCX1VTIjowLCJleHAiOjE1Mzk1MzI4MDV9.f84FB5dff5C-4DYOJjlbc-8_AknQEV31xxdyEZ6rAAE"
        url = "https://t02.io.speechx.cn:8443/MDD_Server/mdd_v18"
        headers = {'Authorization': 'Bearer {0}'.format(api_token)}
        files = dict(myWavfile=file)
        data = dict(word_name=text, myWavefile=filePath, user_id="tingshouPKU")
        response = requests.post(url, files=files, data=data, headers=headers)
        response_json = response.json()
        return response_json