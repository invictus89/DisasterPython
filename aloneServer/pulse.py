# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    Return Reassembled Pulse Data that made official by token
    인증된 토큰을 통해 재조립된 Pulse Data를 Return.    
    호출시 SubProcess 생성
"""
from aloneServer.util import tool, errLog
from flask import request
from multiprocessing import Process, current_process

logger = errLog.ErrorLog.__call__()
t = tool.Tool()

class Pulse(Process):
    def __init__(self, _uri, _q, _key):
        Process.__init__(self)
        self.uri = _uri
        self.q = _q
        self.key = _key
        self.userIP = request.remote_addr
        logger.writeLog("info", "PulseData Call : {0} [{1}]".format(self.userIP, self.key))

    def run(self):
        logger.writeLog("info", "PulseData Assembling....")
        t.setRespJson(self.uri, self.q)

    def __del__(self):
        try:
            logger.writeLog("info", "PulseData Success Return : {0} [{1}]".format(self.userIP, self.key))    
        except:
            pass