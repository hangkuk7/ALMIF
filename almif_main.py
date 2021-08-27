import os
import sys
from datetime import datetime
from datetime import timedelta
from multiprocessing import Process, Queue
from time import sleep

from ConfigManager import ConfManager
from DatabaseManager import DbManager
from LogManager import LogManager
from AlarmManager import AlarmMgr
from ScheduleManager import ScheduleManager
from almif_variables import *

# For SSH
import paramiko
import glob
import getpass
import time

logger = LogManager.getInstance().get_logger()

def initConfig():
    logger.info(f'-------------------- initConfig() --------------------')
    # ALL_CONFIG_INFO = ConfManager.getInstance().get_config_data()

    global LOCAL_CONFIG
    global DB_INFO

    DB_INFO = ConfManager.getInstance().getDbConfig()
    LOCAL_CONFIG = ConfManager.getInstance().getLocalConfig()

    logger.info('LOCAL_CONFIG = {}'.format(LOCAL_CONFIG))
    logger.info('DB_INFO = {}'.format(DB_INFO))

    return True

# multiprocessing function
def proc_alarm_job(alarm_mgr):
    logger.info(f'[PID-{os.getpid()}] *** proc_alarm_job() start! ****')
    alarm_mgr.print_access_info()
    if alarm_mgr.get_remote_alarm() != True:
        logger.critical(f'[PID-{os.getpid()}] Error. get_remote_alarm fail. pid=[{os.getpid()}]')
        return False

    return True

if __name__ == '__main__':

    if len(sys.argv) != 2:
        logger.critical(f"Error. Insufficient arguments")
        sys.exit()

    if sys.argv[1] != MY_PROC_NAME:
        logger.critical(f'Error. Invalid ProcName. ProcName=[{sys.argv[1]}]')
        sys.exit()

    logger.info(f'-------------------- [{MY_PROC_NAME}] Start! --------------------')
    if initConfig() != True:
        logger.critical(f'Error. initConfig() fail')
        sys.exit()

    init_flag = True
    schMgr = ScheduleManager(LOCAL_CONFIG['time_interval'])
    Dbmanager = DbManager(DB_INFO['host'], DB_INFO['user'], DB_INFO['passwd'], DB_INFO['db'])

    while(True)

        if init_flag == True:
            # Initial Processing.
            sql_string = "select * from tb_e2eo_fc_alarm_access_info;"
            logger.debug(f'sql_string=[{sql_string}]')
            db_results = Dbmanager.select(sql_string)
            logger.debug(f'db_results len=[{len(db_results)}], db_results = [{db_results}]')

            alarm_mgr_list = list()
            proc_list = list()
            for result in db_results:
                alarm_mgr = AlarmMgr(result)
                if alarm_mgr != None:
                    alarm_mgr_list.append(alarm_mgr)

                    proc = Process(target=proc_alarm_job, args=(alarm_mgr,))
                    proc_list.append(proc)
                    proc.start()

            for proc in proc_list:
                proc.join()

            init_flag = False
            schMgr.reset_schedule()
        elif init_flag == False and schMgr.check_job_start() == True:
            # select tb_e2eo_fc_alarm_access_info
            sql_string = "select * from tb_e2eo_fc_alarm_access_info;"
            logger.debug(f'sql_string=[{sql_string}]')
            db_results = Dbmanager.select(sql_string)
            logger.debug(f'db_results len=[{len(db_results)}], db_results = [{db_results}]')

            alarm_mgr_list = list()
            proc_list = list()
            for result in db_results:
                alarm_mgr = AlarmMgr(result)
                if alarm_mgr != None:
                    alarm_mgr_list.append(alarm_mgr)

                    proc = Process(target=proc_alarm_job, args=(alarm_mgr,))
                    proc_list.append(proc)
                    proc.start()

            for proc in proc_list:
                proc.join()

            init_flag = False
            schMgr.reset_schedule()
        elif init_flag == False and schMgr.check_job_start() == False:
            sleep(1)
        else:
            sleep(1)

