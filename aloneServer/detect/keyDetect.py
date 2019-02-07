# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    실시간 검색어 Detecting
"""
import requests
from aloneServer import jobs
from aloneServer.util import errLog
from aloneServer.detect import config
from aloneServer.detect.util import checkKeyword
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process
from time import localtime, ctime, strftime, sleep

logger = errLog.ErrorLog.__call__()

class KeyDetect(Process):
    def __init__(self, _title, _url, _config, _format, _q):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format
        self.q = _q   

    def run(self):
        logger.writeLog("info","{0} - Detecting Start.".format(self.title))
        while True:
            try:    #시간 주기는 검색어가 바뀌는 30초단위로
                if localtime().tm_sec == 35 or localtime().tm_sec == 5:
                    if not jobs['DS']:
                        self.detect()
                    else:
                        print("test")
                    sleep(1)
            except BaseException as e:
                logger.writeLog("error", "Keyword Detecting Failed. : {0}".format(e))
                break

    def detect(self):
        lastest_num = 0
        curProcss = self.name
        
        try:
            source_code = requests.get(self.url)
            soup = BeautifulSoup(source_code.text, "html.parser")
            keyList = list()

            for s in soup.select(self.CONFIG['className']):
                keyList.append(s.text)

        except BaseException as e:
            logger.writeLog("error", "{0} - Keyword Detecting Stoped. : {1}".format(self.title, e))
        else:
            checkKeyword(config.Keyward.keywordDic.values(), keyList)
            self.q.put(keyList)
            return "<br>".join(keyList)