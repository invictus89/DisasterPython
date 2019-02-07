# -*- coding: utf-8 -*-
"""
    aloneServer - manager
    ~~~~~

    DB Connection Controller
    APIController가 Query Mapper와 DBController를 
    제어한다.
"""
from aloneServer.db import message, model

#Singleton class
class SingletonType(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonType , cls).__call__(*args, **kwargs)
        return cls._instance[cls]
    
#API Admin
class APIController(metaclass=SingletonType):
    def process(self, _type, *_data):
        #token Key Select
        if _type == "home":
            return_key = str(DBC.selectToken(*_data))
            return return_key
        #token Issue Insert
        elif _type == "auth":
            return message.CompMessage(DBC.insertToken(*_data)).getBool()
        #token Varificate Select
        elif _type == "valid":
            return message.CompMessage(DBC.selectValid(*_data)).getBool()
        #Admin token Varificate Select
        elif _type == "admin":
            return message.CompMessage(DBC.adminValid(*_data)).getBool()
        #Notificated Data Insert
        elif _type == "notice":
            return message.CompMessage(DBC.noticeInsert(*_data)).getBool()
        #earthquake Data Insert
        elif _type == "eqid":
            tmpData = str(DBC.selectEqid()).split(",")
            rsltData = dict()
            rsltData['eqid'] = int(tmpData[0])
            rsltData['time'] = tmpData[1]
            return rsltData
        #word count insert
        elif _type == "wordInsert":
            return message.CompMessage(DBC.insertWord(*_data)).getBool()
        #real time Twit insert
        elif _type == "twitInsert":
            return message.CompMessage(DBC.insertTwit(*_data)).getBool()
        #word Count Select
        elif _type == "wordSelect":
            return DBC.selectWord(*_data).getRows()
        #official data Insert
        elif _type == "dataInsert":
            return message.CompMessage(DBC.insertData(*_data)).getBool()

#DBconnection (Singleton)
class DBController(metaclass=SingletonType):
    def selectToken(self, *_args):
        return model.tokenSelect(_args[0])
    
    def insertToken(self, *_args):
        return model.tokenInsert(_args[0], _args[1])
    
    def selectValid(self, *_args):
        return model.ValidSelect(_args[0])

    def adminValid(self, *_args):
        return model.AdminSelect(_args[0])

    def noticeInsert(self, *_args):
        return model.NoticeInsert(_args[0], _args[1], _args[2], _args[3])

    def selectEqid(self):
        return model.eqidSelect()

    def insertWord(self, *_args):
        return model.wordInsert(_args[0], _args[1])

    def insertTwit(self, *_args):
        return model.twitInsert(_args[0])

    def selectWord(self, *_args):
        return model.wordSelect(_args[0], _args[1])

    def insertData(self, *_args):
        return model.dataInsert(_args[0], _args[1], _args[2])

#instance variable 
APIC = APIController.__call__()
DBC = DBController.__call__()