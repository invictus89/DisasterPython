# -*- coding: utf-8 -*-
"""
    aloneServer
    ~~~~~

    model.
    SQL Query Mapping
"""
from aloneServer.util import errLog
from aloneServer.db import connect
from aloneServer.db.message import SuccessMessage, FailMessage

logger = errLog.ErrorLog.__call__()
db = connect.DBConnect.__call__()

class tokenSelect:
    def __init__(self, _ip="%"):
        self.query = "select ip, AES_DECRYPT(UNHEX(accessKey), 'acorn') from tb_access_auth where ip like '"+_ip+"';"
        self.cur = db.getCursor()
        
        try:
            self.cur.execute(self.query)
            self.isEmpty(self.cur.fetchone())
        except BaseException as e:
            logger.writeLog("error","Token Select Failed. : {0}".format(e))
    
    def isEmpty(self, _row):
        if _row:    #값이 있으면
            self.ip = _row[0]
            self.key = _row[1].decode()
        else:       #값이 없으면
            self.ip = None
            self.key = None

    def __repr__(self):
        return "{0}".format(self.key)

class tokenInsert:
    def __init__(self, _userIP, _encryptKey):
        self.query = "insert into tb_access_auth values ('"+_userIP+"',HEX(AES_ENCRYPT('"+_encryptKey+"','acorn')),sysdate(),'on',null);"
        self.cur = db.getCursor()

        try:
            self.cur.execute(self.query)
            self.returnMsg = SuccessMessage().getMessage()
        except BaseException as e:
            logger.writeLog("error", "Token Insert Error. : {0}".format(e))
            self.returnMsg = FailMessage().getMessage()
        else:
            logger.writeLog("info", "Token Commit Success.")
            db.getDB().commit()

    def __repr__(self):
        return self.returnMsg

class ValidSelect:
    def __init__(self, _accessKey):
        self.query = "select * from tb_access_auth where accessKey = HEX(AES_ENCRYPT('"+_accessKey+"','acorn'));"
        self.cur = db.getCursor()
        
        try:
            self.cur.execute(self.query)
            self.isEmpty(self.cur.fetchone())
        except BaseException as e:
            logger.writeLog("error", "Vailed Select Failed. : {0}".format(e))
        
    def isEmpty(self, _row):
        if _row:    #값이 있으면
            self.returnMsg = SuccessMessage().getMessage()
        else:       #값이 없으면
            self.returnMsg = FailMessage().getMessage()

    def __repr__(self):
        return self.returnMsg

class AdminSelect:
    def __init__(self, _accessKey):
        self.query = "select server_auth from tb_access_auth where accessKey = HEX(AES_ENCRYPT('"+_accessKey+"','acorn'));"
        self.cur = db.getCursor()
        
        try:
            self.cur.execute(self.query)
            self.isEmpty(self.cur.fetchone())
        except BaseException as e:
            logger.writeLog("error", "Admin Select Failed. : {0}".format(e))
        
    def isEmpty(self, _row):
        
        if _row[0] is 1:    #값이 있으면
            self.returnMsg = SuccessMessage().getMessage()
        else:       #값이 없으면
            self.returnMsg = FailMessage().getMessage()

    def __repr__(self):
        return self.returnMsg

class NoticeInsert:
    def __init__(self, _key, _title, _content, _percentage):
        self.query = "insert into tb_notice(time, value, route, content, percentage) values (sysdate(), '"+_key+"', 'Twitter', '"+_content+"', "+_percentage+");"
        self.cur = db.getCursor()
        
        try:
            self.cur.execute(self.query)
            self.returnMsg = SuccessMessage().getMessage()
        except BaseException as e:
            logger.writeLog("error", "Notice Insert Error. : {0}".format(e))
            self.returnMsg = FailMessage().getMessage()
        else:
            logger.writeLog("info", "Notice Commit Success.")
            db.getDB().commit()

    def __repr__(self):
        return self.returnMsg

class eqidSelect:
    def __init__(self):
        self.query = "select max(eqid), max(time) from tb_earthquake_fast_ver2;"
        self.cur = db.getCursor()
        
        try:
            self.cur.execute(self.query)
            self.isEmpty(self.cur.fetchone())
        except BaseException as e:
            logger.writeLog("error","Eqid Select Failed. : {0}".format(e))
    
    def isEmpty(self, _row):
        if _row:    #값이 있으면
            self.maxID = int(_row[0])
            self.time = _row[1]
        else:       #값이 없으면
            self.maxID = 1
            self.time = ""

    def __repr__(self):
        return "{0},{1}".format(self.maxID, self.time)

class wordInsert:
    def __init__(self, _wordDict, _key):
        for k in _wordDict:
            self.query = "insert into tb_word_count values ('"+k+"',"+str(_wordDict[k])+",'"+_key+"',sysdate());"
            self.cur = db.getCursor()
            
            try:
                self.cur.execute(self.query)
                
            except BaseException as e:
                self.up_query = "update tb_word_count set count = count + "+str(_wordDict[k])+", time = sysdate() where word like '"+k+"';"
                self.cur.execute(self.up_query)
                self.returnMsg = SuccessMessage().getMessage()
            else:
                self.returnMsg = SuccessMessage().getMessage()
                #logger.writeLog("info", "Word Commit Success.")
                db.getDB().commit()
    def __repr__(self):
        return self.returnMsg

class twitInsert:
    def __init__(self, _Dict):
        values = ",".join(_Dict.keys())
        placeHolder = ",".join(['%s']*len(_Dict))
        self.query = "insert into tb_twitter_contents ({0}) values ({1});".format(values, placeHolder)
        self.cur = db.getCursor()
        
        try:
            self.cur.execute(self.query, _Dict.values())
        except BaseException as e:
            self.returnMsg = FailMessage().getMessage()
        else:
            self.returnMsg = SuccessMessage().getMessage()    
            db.getDB().commit()
    
    def __repr__(self):
        return self.returnMsg

class wordSelect:
    def __init__(self, _type, _cnt):
        self.query = "select word, count from tb_word_count where type like '"+str(_type)+"' order by count desc limit "+str(_cnt)+";"
        self.cur = db.getCursor()
            
        try:
            self.cur.execute(self.query)    
        except BaseException as e:
            self.returnMsg = FailMessage().getMessage()
        else:
            self.row = self.cur.fetchall()
            self.returnMsg = SuccessMessage().getMessage()

    def __repr__(self):
        return self.returnMsg 

    def getRows(self):
        return self.row

class dataInsert:
    def __init__(self, _columns, _placeholders, _data):
        self.query = "insert into tb_earthquake_fast_ver2 ({0}) values ({1})".format(_columns, _placeholders)
        self.cur = db.getCursor()
            
        try:
            self.cur.execute(self.query,_data.values())
        except BaseException as e:
            self.returnMsg = FailMessage().getMessage()
        else:
            self.returnMsg = SuccessMessage().getMessage()
            db.getDB().commit()
    
    def __repr__(self):
        return self.returnMsg