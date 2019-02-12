# -*- coding: utf-8 -*-
# filename: main.py

import web
from handle import Handle

from web.wsgiserver import CherryPyWSGIServer

ssl_cert = "/usr/src/EEA/2_www.abceea.com.crt"
ssl_key = "/usr/src/EEA/3_www.abceea.com.key"
ssl_chain = "/usr/src/EEA/1_root_bundle.crt"

CherryPyWSGIServer.ssl_certificate = ssl_cert
CherryPyWSGIServer.ssl_private_key = ssl_key
CherryPyWSGIServer.ssl_certificate_chain = ssl_chain


class StaticFile:
    def GET(self, file):
        print file
        web.seeother('/static/' + file);  # 重定向

urls = (
    '/test', 'Handle',
    '(.*\..{1,5})', 'StaticFile',  # 后缀1到5个字母的文件
)

if __name__ == '__main__':
    app = web.application(urls, globals(), True)
    web.internalerror = web.debugerror
    app.run()

