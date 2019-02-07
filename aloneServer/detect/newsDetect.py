# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    News의 키워드들을 Detecting
"""
import requests
from aloneServer import jobs
from aloneServer.util import errLog
from aloneServer.detect import config, dataLoader
from aloneServer.detect.util import checkCount, clearQueue
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process, Queue
from time import localtime, ctime, strftime, sleep

logger = errLog.ErrorLog.__call__()

class NewsDetect(Process):
    def __init__(self, _title, _url, _config, _format, _q):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format
        self.tmp_cnt = 0
        self.q = _q

    def run(self):
        logger.writeLog("info","{0} - Detecting Start.".format(self.title))
        while True:
            try:#분단위 Detecting
                if localtime().tm_sec == 5:
                    self.detect()
                    sleep(1)
            except BaseException as e:
                jobs['news'] = False
                logger.writeLog("error", "NEWS Detecting Failed. : {0}".format(e))

    def detect(self):
        curProcss = self.name
        cnt = None
        clearQueue(self.q)

        try:
            source_code = requests.get(self.url)
            soup = BeautifulSoup(source_code.text, "html.parser")
            
            for s in soup.select(self.CONFIG['className']):
                print(s)
                cnt = s.text[7:-1].replace(",","")
                
        except BaseException as e:
            jobs['news'] = False
            logger.writeLog("error", "{0} - NEWS Detecting Stoped. : {1}".format(self.title, e))
        else:
            gap = self.tmp_cnt-int(cnt)
            content = checkCount(gap, "", "뉴스")
            print("[{0}] {1}-{2}\t{3} ".format(ctime(), curProcss, self.title, content))
            self.q .put(content)
            loader = dataLoader.DataLoader(2017)
            loader.start()
            loader.join()
            self.tmp_cnt = int(cnt)