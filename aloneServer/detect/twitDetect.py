# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    Twitter 실시간 Streaming Detect
    socket통신 을 담당한다
"""
import json
from aloneServer.util import errLog
from aloneServer.detect import config
from aloneServer.detect.wordAnalysis import WordAnalysis
from aloneServer.detect.util import *
from time import strptime, ctime, time
from datetime import datetime, timedelta
from multiprocessing import Process, current_process, Queue
from tweepy import API, Stream, OAuthHandler
from tweepy.streaming import StreamListener

logger = errLog.ErrorLog.__call__()

class TwitDetect(Process):
    def __init__(self, _title, _url, _config, _format, _sock, _q, _kq):
        Process.__init__(self)
        self.title = _title
        self.url = _url
        self.CONFIG = _config
        self.min_format = _format
        
        self.curProcss = self.name
        keyword = []

        for value in config.Keyward.keywordDic.values():
            for k in value:
                keyword.append(k) 

        auth = OAuthHandler(config.Key_Config.consumerKey, config.Key_Config.consumerSecret)
        auth.set_access_token(config.Key_Config.accessToken, config.Key_Config.accessTokenSecret)
        api = API(auth, wait_on_rate_limit=True, wait_on_rate_limit_notify=True, retry_count=10, retry_delay=5, retry_errors=5)

        l = Listener(self.title, self.curProcss, self.min_format, config.Keyward.keywordDic, _sock, api, _q, _kq)
        try: 
            twitterStream = Stream(api.auth, l)
            twitterStream.filter(track=keyword, async=True) 
            
        except BaseException as e:
            logger.writeLog("error","{0} : Twitter Stream Error".format(e))

    def run(self):
        pass

class Listener(StreamListener):
    def __init__(self, _title, _process, _format, _keywordDic, _sock, _api, _q, _kq):
        self.title = _title
        self.curProcess = _process
        self.format = _format
        self.tmp_time = time()
        self.sockio = _sock 

        self.keywordDic = _keywordDic
        self.counting = setInitial(self.keywordDic)
        self.str_text = setInitialStr(self.keywordDic)
        self.api = _api

        self.q = _q
        self.kq = _kq
    def on_connect(self):
        logger.writeLog("info","{0} - Detecting Start.".format(self.title))
    
    def on_data(self, raw_data):
        data = json.loads(raw_data)
        utctime = datetime.strptime(data['created_at'], self.format)
        kor_time = utctime + timedelta(hours=9)
        
        twitSave(self.sockio, data, str(kor_time))
        
        if not self.q.empty():
            cont = self.q.get()
            sendNews("News", self.sockio, cont)

        if not self.kq.empty():
            cont = self.kq.get()
            sendNews("Key",self.sockio, cont)

        if 'retweeted_status' in data:
            pass
        else:
            for i, k in enumerate(self.keywordDic.values()):
                for value in k:
                    if value in data['text']:
                        setString(self.str_text, i, data['text'])
                        setCounting(self.counting, i)
                
                if isOneMin(self.tmp_time):
                    for i, k in enumerate(self.counting):
                        tmp_data = Queue()
                        
                        wordProcess = WordAnalysis(self.str_text.get(k), tmp_data)
                        wordProcess.start()
                        wordProcess.join()
                    
                        if k == "지진":
                            stuff = self.api.user_timeline(screen_name='KMA_earthquake', count = 5, include_rts = False)
                            sendOfficial(self.sockio, stuff)
                
                        print("[{0}] {1}-{2}({3})\t{4}".format(ctime(), self.curProcess, self.title, k, checktwitCount(self.sockio, self.counting.get(k), k, self.tmp_time, tmp_data.get())))

                    self.tmp_time = time()
                    resetCount(self.counting)
                    resetString(self.str_text)

    def keep_alive(self):
        try:
            pass
        except ConnectionAbortedError as c:
            logger.writeLog("info","{0} - Detecting Stoped. : {1}".format(self.title, c))

    def on_error(self, _status):
        logger.writeLog("error","Twitter Detecting Error. : {0}".format(_status))
