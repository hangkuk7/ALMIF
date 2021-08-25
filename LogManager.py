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
        if len(log_name) < 1:
            print(f'Invalid log name. log_name=[{log_name}]')
            return None

        if len(log_dir) < 1:
            print(f'Invalid log dir. log_dir=[{log_dir}]')
            return None

        self._log_name = log_name
        self._log_dir = log_dir
        self._log_suffix = '_log-%Y-%m-%d'

        self.logger = logging.getLogger(self._log_name)
        # To do later. set log level.
        self.logger.setLevel(logging.DEBUG)

        # Create Log Directory
        if not os.path.exists(self._log_dir):
            os.makedirs(self._log_dir)
            print(f'Make Log Directory. log_dir=[{self._log_dir}]')

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
        self.fileHandler.suffix = self._log_suffix
        #formatter
        self.formatter = logging.Formatter('[%(asctime)s.%(msecs)03d] %(levelname)s %(message)s')
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

