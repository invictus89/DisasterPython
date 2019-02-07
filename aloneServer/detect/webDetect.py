import requests
from aloneServer.util import errLog
from aloneServer.detect.util import _get_article_Time, checkCount
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process
from time import localtime, ctime, strftime, sleep

logger = errLog.ErrorLog.__call__()

class WebDetect(Process):
    def __init__(self, _title, _url, _config, _format):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format

    def run(self):
        logger.writeLog("info","{0} - Detecting Start.".format(self.title))
        while True:
            try:
                if localtime().tm_sec == 59:
                    self.detect(self.min_format, self.CONFIG, self.title, self.url)
                    sleep(1)
            except BaseException as e:
                logger.writeLog("error", "WebDetecting Failed. : {0}".format(e))
                break

    def detect(self, _minFormat, _config, _title, _url):
        lastest_num = 0
        creteria = strftime(_minFormat, localtime())
        curProcss = current_process().name
        
        try:
            source_code = requests.get(_url)
            plain_code = source_code.text
            soup = BeautifulSoup(plain_code, "html.parser")
            
            for target_text in soup.select(_config['rowName']):
                if _get_article_Time(target_text, _config, _minFormat) == creteria:
                    lastest_num += 1
        except BaseException as e:
            logger.writeLog("error", "{0} - WebDetecting Stoped. : {1}".format(_title, e))
        else:
            #logger.writeLog("info","{0}\t{1} ".format(_title, checkCount(lastest_num, _title, "지진")))
            print("[{0}] {1}-{2}\t{3} ".format(ctime(), curProcss, _title, checkCount(lastest_num, _title, "지진")))