# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    각종 재난등의 증상 발생시 Official Data Load
"""
import requests
import re
from aloneServer.util import errLog
from aloneServer.detect.util import _get_article_Time, getMaxEQID
from bs4 import BeautifulSoup
from multiprocessing import Process, current_process
from time import localtime, ctime, strftime, sleep, strptime

logger = errLog.ErrorLog.__call__()

class DataLoader(Process):
    def __init__(self, _year):
        Process.__init__(self)
        self.year = str(_year)
    
    def __del__(self):
        logger.writeLog("info", "Data Searching Finished.]")    

    def run(self):
        logger.writeLog("info","{0} - Data Searching Start.".format("지진"))
        
        try:
            self.dataSearch(self.year)
        except BaseException as b:
            logger.writeLog("error", "Data Searching Failed. : {0}".format(b))

    def dataSearch(self, _year):
        from aloneServer.manager import APIC
        
        ori_url = "http://www.kma.go.kr"
        cnt = getMaxEQID()['eqid']+1
        try:
            _url = ori_url+ "/weather/earthquake_volcano/domesticlist.jsp?startSize=0&endSize=10&pNo=1&startTm=" + str(_year + "-01-01") + "&endTm=" + str(_year + "-12-31")
            source_code = requests.get(_url)
            soup = BeautifulSoup(source_code.text, "html.parser")

            for s in soup.select('table.table_develop > tbody > tr'):
                if self._get_Time(s) == getMaxEQID()['time']:
                    break
                data = {'time':self._get_Time(s),'degree':self._get_Degree(s),'title':self._get_Title(s),'lat':self._get_Lat(s).strip(),'lng':self._get_Lng(s).strip(),'tag':self._get_Tag(ori_url,s),'FirstAdd':self._get_Title(s).split(' ')[0],'SecondAdd':self._get_Title(s).split(' ')[1],'DetailAdd':" ".join(self._get_Title(s).split(' ')[2:])}
                self.spider(self._get_Time(s), _year, data)
                data['eqid'] = cnt
                
                try:
                    columns = ','.join(data.keys())
                    placeholders = ','.join(['%s'] * len (data))
                    APIC.process("dataInsert", columns, placeholders, data)
                    cnt += 1
                except BaseException as e:
                    logger.writeLog("error", "{0} - Data Insert Failed. : {1}".format("지진", e))
        except BaseException as e:
            logger.writeLog("error", "{0} - Data Searching Stoped. : {1}".format("지진", e))
        else:
            logger.writeLog("info", "{0} - Data Insert Success.".format("지진"))

    def spider(self, _time, _year, _data):
        url = "http://necis.kma.go.kr/necis-dbf/user/earthquake/annual_earthquake_list.do?pageIndex=1&cal_url=%2Fnecis-dbf%2Fsym%2Fcal%2FEgovNormalCalPopup.do&closeYnCheck=&pSort=&pOrderBy=&locationCheckBox=%EC%84%9C%EC%9A%B8&locationCheckBox=%EA%B2%BD%EA%B8%B0&locationCheckBox=%EC%9D%B8%EC%B2%9C&locationCheckBox=%EB%B6%80%EC%82%B0&locationCheckBox=%EA%B2%BD%EB%82%A8&locationCheckBox=%EC%9A%B8%EC%82%B0&locationCheckBox=%EB%8C%80%EA%B5%AC&locationCheckBox=%EA%B2%BD%EB%B6%81&locationCheckBox=%EA%B4%91%EC%A3%BC&locationCheckBox=%EC%A0%84%EB%82%A8&locationCheckBox=%EC%A0%84%EB%B6%81&locationCheckBox=%EB%8C%80%EC%A0%84&locationCheckBox=%EC%B6%A9%EB%82%A8&locationCheckBox=%EC%B6%A9%EB%B6%81&locationCheckBox=%EA%B0%95%EC%9B%90&locationCheckBox=%EC%A0%9C%EC%A3%BC&locationCheckBox=%EB%B6%81%ED%95%9C&locationCheckBox=%EA%B8%B0%ED%83%80&seaCheckBox=130&seaCheckBox=110&seaCheckBox=120&magnitudeFrom=&magnitudeTo=&latitudeFrom=&latitudeTo=&longitudeFrom=&longitudeTo=&stdYear="+str(_year)+"&endYear="+str(_year)+"&searchWord="
        source_code = requests.get(url)
        soup = BeautifulSoup(source_code.text, 'html.parser')
        for tr in soup.select('table.obsTable tbody tr'):
            if self._get_target_time(tr) == _time:
                _data['url'] = self._get_pulse_url(tr)
                return True
            else:
                _data['url'] = ""

    def _get_Time(self, _plainText):
        for i, td in enumerate(_plainText.select('td')):
            if i == 1:
                try:
                    return strftime('%Y-%m-%d %H:%M:%S', strptime(td.text, '%Y/%m/%d %H:%M:%S'))
                except:
                    return None
    def _get_target_time(self, _plainText):
        for time_tag in _plainText.select('td:nth-of-type(2)'):
            return time_tag.text


    def _get_Degree(self, _plainText):
        for i, td in enumerate(_plainText.select('td')):
            if i == 2:
                return td.text

    def _get_Title(self, _plainText):
        for i, td in enumerate(_plainText.select('td')):
            if i == 6:
                return td.text

    def _get_Lat(self, _plainText):
        for i, td in enumerate(_plainText.select('td')):
            if i == 4:
                return td.text[:-2]

    def _get_Lng(self, _plainText):
        for i, td in enumerate(_plainText.select('td')):
            if i == 5:
                return td.text[:-2]

    def _get_Tag(self, _origin ,_plainText):
        c = re.compile(r'(/\D+[a-zA-Z0-9_]+.png)')
        if not len(_plainText.select('a')) == 0:
            for tag in _plainText.select('a'):
                plain_text = str(tag['onclick'])
                src_img = c.findall(plain_text)
                return _origin + src_img[0]
        else:
            return ""

    def _get_pulse_url(self, _plainText):
        if not len(_plainText.select('a:nth-of-type(2) > img')) == 0:
            for pulseParam in _plainText.select('a:nth-of-type(2) > img'):
                a = re.sub("'","",pulseParam['onclick'][13:-2]).split(",")
                u = "http://necis.kma.go.kr/necis-dbf/usernl/earthquake/eventwavefileread.do?eqId="+a[0].strip()+"&eqDt="+re.sub(" ","+",a[1].strip())+"&lat=++"+a[2].strip()+"&lon=+"+a[3].strip()+"&staCnt=5&fileFullPath="+a[4].strip()
                return u
        else:
            return ""
