# -*- coding: utf-8 -*-
# filename: main.py

import json

#
import requests
import time

class wxServer:
    def __init__(self):
        self.access_token = str()
        self.lastTime = time.time()
        self.session = requests.session()
        self.getAccessToken()

    def getAccessToken(self):
        url = "https://api.weixin.qq.com/cgi-bin/token?grant_type=client_credential&appid=wxc14f34923223ee96&secret=02e6e0b9a69784477e392ab9df9f64e4"
        res = self.session.get(url)
        txt = json.loads(res.text.encode('utf-8'))
        self.access_token = txt["access_token"]
        print(self.access_token)

        '''
            点评时间
            {{keyword1.DATA}}
            学员姓名
            {{keyword2.DATA}}
            班级名称
            {{keyword3.DATA}}
            练习话题
            {{keyword4.DATA}}
            点评内容
            {{keyword5.DATA}}
            点评者
            {{keyword6.DATA}}
        '''

    def postMessageToUser(self, openId, formId, url, commentTime, punchHostName, className, courseContent, commentContent, commmentName):
        if int(time.time()) - int(self.lastTime) > 7200:
            self.getAccessToken()
        param = {
          "touser": openId,
          "template_id": "UKpJ0eLqi_3ZddZ9j16X1rKBtHvak_CQNN36MVDw_Ak",
          "page": url,
          "form_id": formId,
          "data": {
              "keyword1": {
                  "value": commentTime
              },
              "keyword2": {
                  "value": punchHostName
              },
              "keyword3": {
                  "value": className
              },
              "keyword4": {
                  "value": courseContent
              },
              "keyword5": {
                  "value": commentContent
              },
              "keyword6": {
                  "value": commmentName
              }
          }
        }
        #print("template param: ", param)
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + self.access_token
        res = self.session.post(url, json.dumps(param))
        #print("template res: ", res)
        print("template text: ", res.text)
        txt = json.loads(res.text.encode('utf-8'))

        '''
        活动名称
        {{keyword1.DATA}}
        提示语
        {{keyword2.DATA}}
        已打卡次数
        {{keyword3.DATA}}
        提醒时间
        {{keyword4.DATA}}
        '''

    def postNotificationToUser(self, openId, formId, url, notice):
        if int(time.time()) - int(self.lastTime) > 7200:
            self.getAccessToken()

        localtime = time.asctime(time.localtime(time.time()))
        param = {
          "touser": openId,
          "template_id": "NaXJiVFdvdLEWVQLpHtRKGPxXBwzJr7H1O8mody_kzQ",
          "page": url,
          "form_id": formId,
          "data": {
              "keyword1": {
                  "value": "听说无忧，听说有你"
              },
              "keyword2": {
                  "value": "可爱的小伙伴都在等着你呢~快点击直接进入吧->"
              },
              "keyword3": {
                  "value": notice
              },
              "keyword4": {
                  "value": localtime
              },
          }
        }
        #print("template param: ", param)
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + self.access_token
        res = self.session.post(url, json.dumps(param))
        #print("template res: ", res)
        print("template text: ", res.text)
        txt = json.loads(res.text.encode('utf-8'))
        return txt

    def postVersionChangeToUser(self, openId, formId, url, notice):
        if int(time.time()) - int(self.lastTime) > 7200:
            self.getAccessToken()

        localtime = time.asctime(time.localtime(time.time()))
        param = {
          "touser": openId,
          "template_id": "NaXJiVFdvdLEWVQLpHtRKGPxXBwzJr7H1O8mody_kzQ",
          "page": url,
          "form_id": formId,
          "data": {
              "keyword1": {
                  "value": "版本更新"
              },
              "keyword2": {
                  "value": "1.打卡，点评，点赞均可获赠小红花。2.即刻起可以给你喜欢的小伙伴送花啦"
              },
              "keyword3": {
                  "value": notice
              },
              "keyword4": {
                  "value": localtime
              },
          }
        }
        #print("template param: ", param)
        url = "https://api.weixin.qq.com/cgi-bin/message/wxopen/template/send?access_token=" + self.access_token
        res = self.session.post(url, json.dumps(param))
        #print("template res: ", res)
        print("template text: ", res.text)
        txt = json.loads(res.text.encode('utf-8'))
        return txt