import MySQLdb
from aloneServer.db.config import DB_Config
from aloneServer.util import errLog

logger = errLog.ErrorLog.__call__()

class Single(type):
    _instance = {}
    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            cls._instance[cls] = super(Single, cls).__call__(*args, **kwargs)
        return cls._instance[cls]

class DBConnect(metaclass=Single):
    _DB = None
    _Cursor = None

    def __init__(self):
        try:
            self._DB = MySQLdb.connect(**DB_Config.db_config)
        except BaseException as d:
            logger.writeLog("critical","DB Connect Failed. : {0}".format(b))
        else:
            logger.writeLog("info","DB Connected. : {0}".format(self._DB))
    
    def setCursor(self, _cursor):
        if self._Cursor == None:
            self._Cursor = _cursor

    def getDB(self):
        return self._DB

    def getCursor(self):
        if self._Cursor == None:
            self._Cursor = self._DB.cursor()
            return self._Cursor
        else:
            return self._Cursor