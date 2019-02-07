# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    View Controller
    Flask서버의 전체적인 view 관리
    a.k.a Servlet
"""
import requests
import json

from aloneServer.util import errLog
from flask import abort
from re import sub, compile
from hashlib import md5
from time import time, ctime, sleep

logger = errLog.ErrorLog.__call__()
"""
    HTTPError
    parameter : 
        1] HTTP 상태코드
        2] Message
        3] Ip address
    description :
        HTTP에서 처리 및 로깅
"""
def HTTPError(_statusCode, _msg, _ip=None):
    logger.writeLog("warning", "[{0}]{1} : {2}".format(_statusCode, _msg, _ip))
    return abort(_statusCode, 'Access Denied. '+str(_msg))
"""
    grey_color_func
    parameter :
        wordcloud package 내장
    description :
        wordcloud 색상함수
"""
def grey_color_func(word, font_size, position, orientation, random_state=None,**kwargs):
    from random import randint
    return "hsl({0}, {1}%, {2}%)".format(50,randint(30, 100),randint(20, 50))
"""
    Tool Class
    
    * description :
        Pulse assemble 전용 함수 Class
"""
class Tool():
    def setRespJson(self, _uri, _output):
        result = []
        url = _uri
        source = requests.get(url).json()
        s = str(source['rtn_result'])

        if s == None:
            logger.writeLog("info", 'No Data')
            return False
    
        plain_text = s.split('||')
        c = compile(r"(\d+).(\d+),(.?\d+)")
        met = c.findall(plain_text[0])
    
        for a in met:
            timestamp = a[0]+""+a[1][:3]
            data = {"time":int(timestamp),"value":str(a[2])}
            result.append(data)
    
        sortedResult = sorted(result, key=self.getTime, reverse=False)
        _output.put(json.dumps(sortedResult))

    def getTime(self, _n):
        return int(_n.get('time'))
"""
    Encrypt
    
    * description :
        ip address encryption method
"""
class Encrypt:
    def keyEncrypt(self,_IP):
        plain_text = int(sub("\.","",str(_IP)))+int(sub("\.","", str(time()))[-12:])
        encrypt = md5(str(plain_text).encode()).hexdigest()        
        return encrypt

