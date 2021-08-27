from datetime import datetime
from datetime import timedelta

from LogManager import LogManager

# For log
logger = LogManager.getInstance().get_logger()

class ScheduleManager:
    def __init__(self, interval):
        if interval < 1:
            logger.critical(f'[ScheduleManager init] Error. Invalid interval=[{interval}]')
            return None

        self._interval = interval
        self._current_time = datetime.now()
        self._next_time = self._current_time + timedelta(seconds=self._interval)
        self._str_current_time = self._next_time.strftime('%Y-%m-%d %H:%M:%S')
        self._str_next_time = self._next_time.strftime('%Y-%m-%d %H:%M:%S')

    def check_job_start(self):
        self._current_time = datetime.now()
        if self._current_time >= self._next_time:
            logger.info(f'**** Job Start! *****')
            self.print_schedule_time()
            return True
        else:
            return False

    def reset_schedule(self):
        self._current_time = datetime.now()
        self._next_time = self._current_time + timedelta(seconds=self._interval)
        self.print_schedule_time()

    def print_schedule_time(self):
        self._str_current_time = self._current_time.strftime('%Y-%m-%d %H:%M:%S')
        self._str_next_time = self._next_time.strftime('%Y-%m-%d %H:%M:%S')
        logger.info(f'current_time=[{self._str_current_time}], next_time=[{self._str_next_time}]')