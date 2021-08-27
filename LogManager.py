import datetime
import logging
import logging.handlers
import os
import sys
from almif_variables import *
from ConfigManager import ConfManager

LOCAL_CONFIG = ConfManager.getInstance().getLocalConfig()

class LogManager:

    __instance = None
    logger = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if LogManager.__instance == None:
            LogManager.__instance = LogManager()
        return LogManager.__instance

    def __init__(self):

        self._log_name = MY_LOG_FILE_NAME
        try:
            home_str = os.environ["HOME"]
            print("[LogManager init] HOME : " + str(home_str))
        except KeyError:
            print("[LogManager init] Error. Please set the environment variable HOME")
            return None

        self._log_dir = '%s/log/%s' % (home_str, MY_PROC_NAME)
        print(f'[LogManager init] self._log_dir = [{self._log_dir}]')
        self._log_suffix = '%Y-%m-%d'

        self.logger = logging.getLogger(self._log_name)

        conf_log_level = LOCAL_CONFIG['msg_log_level']
        print(f'[LogManager init] conf_log_level = [{conf_log_level}]')
        self._log_level = logging.DEBUG
        if conf_log_level < 1:
            self._log_level = logging.DEBUG
        elif conf_log_level == CONFIG_LOG_LEVEL_CRITICAL:
            self._log_level = logging.CRITICAL
        elif conf_log_level == CONFIG_LOG_LEVEL_ERROR:
            self._log_level = logging.ERROR
        elif conf_log_level == CONFIG_LOG_LEVEL_WARNING:
            self._log_level = logging.WARNING
        elif conf_log_level == CONFIG_LOG_LEVEL_INFO:
            self._log_level = logging.INFO
        elif conf_log_level == CONFIG_LOG_LEVEL_DEBUG:
            self._log_level = logging.DEBUG
        else:
            self._log_level = logging.DEBUG

        print(f'[LogManager init] self._log_level = [{self._log_level}]')
        self.logger.setLevel(self._log_level)

        # Create Log Directory
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)
            print(f'[LogManager init] Make Log Directory. log_dir=[{self._log_dir}]')

        self.set_fileHandler()

    def set_fileHandler(self):

        # 10 MB ( Automation File Control )
        # self.fileHandler = logging.handlers.RotatingFileHandler(filename=fileLoc, maxBytes=maxSize, backupCount=maxBackupCnt, encoding='utf-8')
        log_file_name = '%s/%s' % (self._log_dir, self._log_name)
        print(f'log_file_name=[{log_file_name}]')
        self.fileHandler = logging.handlers.TimedRotatingFileHandler(
            filename=log_file_name,
            when='midnight',
            interval=1,
            encoding='utf-8'
        )

        self.formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s')
        self.fileHandler.setFormatter(self.formatter)
        self.fileHandler.suffix = self._log_suffix

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

