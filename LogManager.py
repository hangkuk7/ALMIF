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


