import os
import sys
from multiprocessing import Process, Queue

from ConfigManager import ConfManager
from DatabaseManager import DbManager
from LogManager import LogManager
from AlarmManager import AlarmMgr
from almif_variables import *

# For SSH
import paramiko
import glob
import getpass
import time

def initConfig():
    print(f'-------------------- initConfig() --------------------')
    print(f'--------------------Get Config--------------------')
    # ALL_CONFIG_INFO = ConfManager.getInstance().get_config_data()

    global LOCAL_CONFIG
    global DB_INFO

    DB_INFO = ConfManager.getInstance().getDbConfig()
    LOCAL_CONFIG = ConfManager.getInstance().getLocalConfig()

    print('LOCAL_CONFIG = {}'.format(LOCAL_CONFIG))
    print('DB_INFO = {}'.format(DB_INFO))

    return True

def initLog():
    print(f'initLog Start!')

    # Set Log name.
    log_name = myProcName + "_log"
    print(f'[initLog] log_name = [{log_name}]')

    # Set Log Directory.
    try:
        home_str = os.environ["HOME"]
        print("[initLog] HOME : " + str(home_str))
    except KeyError:
        print("[initLog] Error. Please set the environment variable HOME")
        return False

    # log_dir =

    return True

# multiprocessing function
def proc_alarm_job(alarm_mgr):
    print(f'*** proc_alarm_job() start! pid=[{os.getpid()}]****')
    alarm_mgr.print_access_info()
    if alarm_mgr.get_remote_alarm() != True:
        print(f'Error. get_remote_alarm fail. pid=[{os.getpid()}]')

    return True

if __name__ == '__main__':
    print(f'ALMIF main() start')
    print(f'sys.argv len = [{len(sys.argv)}]')

    global myProcName
    # set Process Name
    myProcName = 'ALMIF'

    if len(sys.argv) != 2:
        print(f"Error. Insufficient arguments")
        sys.exit()

    if sys.argv[1] != myProcName:
        print(f'Error. Invalid ProcName. ProcName=[{sys.argv[1]}]')
        sys.exit()

    print(f'***** {myProcName} Start! *****')
    if initConfig() != True:
        print(f'Error. initConfig() fail')
        sys.exit()

    if initLog() != True:
        print(f'Error. initLog() fail')
        sys.exit()

    # select tb_e2eo_fc_alarm_access_info
    Dbmanager = DbManager(DB_INFO['host'], DB_INFO['user'], DB_INFO['passwd'], DB_INFO['db'])
    sql_string = "select * from tb_e2eo_fc_alarm_access_info;"
    print(f'sql_string=[{sql_string}]')
    db_results = Dbmanager.select(sql_string)
    print(f'db_results len=[{len(db_results)}], db_results = [{db_results}]')

    alarm_mgr_list = list()
    proc_list = list()
    for result in db_results:
        alarm_mgr = AlarmMgr(result)
        if alarm_mgr != None:
            # alarm_mgr.print_access_info()
            alarm_mgr_list.append(alarm_mgr)

            proc = Process(target=proc_alarm_job, args=(alarm_mgr,))
            proc_list.append(proc)
            proc.start()

    for proc in proc_list:
        proc.join()

