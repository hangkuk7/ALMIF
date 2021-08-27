from datetime import datetime
from datetime import timedelta

from LogManager import LogManager

# For log
logger = LogManager.getInstance().get_logger()

class ScheduleManager:
    def __init__(self, interval):
        if interval < 1:
            logger.critical(f'[ScheduleManager init] Error. Invalid interval. interval=[{interval}]')
            return None



        pass

    def set_fileHandler(self):
        pass