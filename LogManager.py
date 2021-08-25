import datetime
import logging
import logging.handlers
import os
import sys

class LogManager:

    __instance = None
    logger = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if LogManager.__instance == None:
            LogManager.__instance = LogManager()
        return LogManager.__instance

    def __init__(self, log_name, log_dir):

        self.logger = logging.getLogger("msglog")
        self.logger.setLevel(logging.DEBUG)

        currentDate = datetime.datetime.now()
        current     = currentDate.strftime('%Y-%m-%d')

        self.set_fileHandler(current)

    def set_fileHandler(self, current):

        maxSize         = 10400
        maxBackupCnt    = 10

        try:
            home_str = os.environ["HOME"]
        except:
            home_str = '/data1/e2e'

        # File
        dirLoc  = '%s/log/MSG_LOG/SYNC/%s' % (home_str , current)
        fileLoc = dirLoc + "/pyscript_file.log"

        if not os.path.exists(dirLoc):
            os.makedirs(dirLoc)

        # 10 MB ( Automation File Control )
        self.fileHandler = logging.handlers.RotatingFileHandler(filename=fileLoc, maxBytes=maxSize, backupCount=maxBackupCnt, encoding='utf-8')

        #formatter
        self.formatter = logging.Formatter('[%(asctime)s|%(filename)s:%(lineno)s][%(levelname)s] > %(message)s')
        self.fileHandler.setFormatter(self.formatter)
        self.logger.handlers = []
        self.logger.addHandler(self.fileHandler)

    # def updateLogLoc(self):
    #
    #     currentDate = datetime.datetime.now()
    #
    #     if  currentDate.strftime('%H:%M:%S') == "00:00:00":
    #
    #         current = currentDate.strftime('%Y-%m-%d')
    #         LogManager.getInstance().set_fileHandler(current)

    def get_logger(self):
        # type: () -> object
        return self.logger

