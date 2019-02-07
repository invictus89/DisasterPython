# -*- coding:utf-8 -*-
from time import time, strptime, strftime, ctime

def checktwitCount(_sock, _count, _key, _tmptime, _wc):
    from aloneServer.manager import APIC
    
    percentage = (_count / 10) * 100
    try:
        if percentage > 0:#수치조정 필요
            content = "발생 추정 : {0}".format(_count)
            APIC.process("notice", _key, "twitter", content[:5], str(int(percentage)))
            APIC.process("wordInsert", _wc, _key)
            _sock.emit("notification", {"percentage":percentage,"message":content[:5],"type":_key,"wordcloud":_wc,"time":strftime("%Y/%m/%d %a %H:%M:%S", strptime(ctime(_tmptime)))}, broadcast=True)
        elif percentage == 0:
            content = "안전 상태 : {0}".format(_count)
        else:
            content = "발생 가능성 ["+str(percentage)+"%] : {0}".format(_count)
    except Exception as e:
        print(e)
    else:
        return content

def twitSave(_sock, _twitJSON, _korTime):
    from aloneServer.manager import APIC
    data = dict()
    tag = list()
    
    try:
        for txt in _twitJSON['entities']['hashtags']:
            tag.append(txt['text'])

        data['time'] = _korTime
        data['tag'] = ",".join(tag)
        data['text'] = _twitJSON['text']
        data['profileURL'] = _twitJSON['user']['profile_image_url_https']
        data['name'] = _twitJSON['user']['screen_name']
        data['timeZone'] = _twitJSON['user']['time_zone']
        data['location'] = _twitJSON['user']['location']
        
        if not _twitJSON['retweeted']:
            APIC.process("twitInsert", data)
        
        _sock.emit("twitter", data, broadcast=True)
    except BaseException as e:
        print(e)

def sendOfficial(_sock, _status):
    inner = list()
    outter = list()

    for status in _status:
        textStr = status._json['text']
        tmp = textStr.split(' ')
        if boolLocation(textStr):
            data = dict()
            data['type'] = "국내"+tmp[0][1:-3]
            data['text'] = " ".join(tmp[1:-1])
            inner.append(data)
        else:
            data = dict()
            data['type'] = tmp[0][1:-3]
            data['text'] = " ".join(tmp[1:-2])[:-1]
            outter.append(data)

    _sock.emit("official", {"inner":inner[0],"outter":outter[0]}, broadcast=True)

def sendNews(_type ,_sock, _content):
    print("[{0}]{1} ==> Send Data...".format(ctime(), _type))
    _sock.emit(_type, {"type":_type, "message":_content, "time":strftime("%Y/%m/%d %a %H:%M:%S", strptime(ctime()))}, broadcast=True)

def boolLocation(_text):
    from re import sub, compile
    c = compile(r"\[\D+\]")
    met = c.findall(_text)
    
    if met[0][1:-1] == "지진정보":
        return True
    else:
        return False
    
def isOneMin(_time):
    return time() - _time > 59

def setInitial(_dic):
    result = dict()
    for i, key in enumerate(_dic.keys()):
        result[key] = 0
    return result

def setInitialStr(_dic):
    result = dict()
    for i, key in enumerate(_dic.keys()):
        result[key] = " "
    return result

def setString(_Str , _index, _data):
    for i,key in enumerate(_Str.keys()):
        if i == _index:
            tmp = _Str.get(key)
            _Str[key] =  tmp + str(_data)

def setCounting(_counting , _index):
    for i,key in enumerate(_counting.keys()):
        if i == _index:
            tmp = _counting.get(key)
            _counting[key] = int(tmp) + 1

def resetString(_Str):
    for i,key in enumerate(_Str.keys()):
        _Str[key] = " "  
        
def resetCount(_counting):
    for i,key in enumerate(_counting.keys()):
        _counting[key] = 0

def _get_article_Time(_itemTag, _config, _format):
    format = '%Y.%m.%d %H:%M:%S'
    tdSelect = _itemTag.select(_config['className'])
    for td in tdSelect:
        if _config['attr']:
            try:
                time_String = td.get(_config['attr']) if td.get(_config['attr']) != None else '0'
                return strftime(_format, strptime(time_String, format)) if time_String != '0' else False
            except BaseException as e:
                pass
        else:
            try:
                time_String = td.text.strip()
                return strftime(_format, strptime(time_String, _format))
            except BaseException as e:
                pass
            
def checkCount(_count, _route, _key):
    from aloneServer.manager import APIC
    percentage = (_count / 10) * 100
    try:
        if percentage > 20:#수치조정 필요
            content = "발생 추정"
            #APIC.process("notice", _key, "Web", content, str(int(percentage)))
        elif percentage == 0:
            content = "안전 상태"
        else:
            content = "발생 가능성 ["+str(percentage)+"%]"
    except Exception as e:
        print(e)
    else:
        return content

def checkKeyword(_config, _keylist):
    for value in _config:
        for k in value:
            if k in _keylist:
                print(k) 
            else:
                return False

def getMaxEQID():
    from aloneServer.manager import APIC
    return APIC.process("eqid")

def clearQueue(_q):
    while not _q.empty():
        _q.get()