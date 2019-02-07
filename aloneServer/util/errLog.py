# -*- coding: utf-8 -*-
"""
    util Logging
    ~~~~~~~~~~~~~~
    
    Singleton pattern Class
    logging class based on logging
"""
from aloneServer.util.config import format_Config

import logging
from logging import Formatter
#from logging.handlers import RotatingFileHandler

#Singleton class
class SingletonType(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(SingletonType , cls).__call__(*args, **kwargs)
        return cls._instance[cls]

class ErrorLog(metaclass=SingletonType):
    """
        Level	    Numeric value
        CRITICAL	50
        ERROR	    40
        WARNING	    30
        INFO	    20
        DEBUG	    10
        NOTSET	    0
    """
    #Logger Variable
    _logger = None
    
    def __init__(self):
        self._logger = logging.getLogger("serverLogger")
        self._logger.setLevel(10)

        fileHandler = logging.FileHandler(**format_Config.serverLog)
        fileHandler.setFormatter(Formatter(format_Config.server_format))
        streamHandler = logging.StreamHandler()
        streamHandler.setFormatter(Formatter(format_Config.stream_format))

        self._logger.addHandler(fileHandler)
        self._logger.addHandler(streamHandler)

    def getLogger(self):
        return self._logger

    def writeLog(self, mode, msg=None):
        """
            전달 mode에 따라 logging.
            critical : 서버운영에 지장을 주는 정도
            error : 서버운영은 유지되지만 기능에 지장이 생기는 정도
            warning : 서버운영은 유지되지만 기능적 제한이 생기는 정도
            info : 서버운영 알림
        """
        if mode is "critical":
            self._logger.critical(msg)
        elif mode is "error":
            self._logger.error(msg)
        elif mode is "warning":
            self._logger.warning(msg)
        elif mode is "info":
            self._logger.info(msg)