import os
import sys
from multiprocessing import Process, Queue

from ConfigManager import ConfManager
from DatabaseManager import DbManager

# define global variables
global myProcName


def initConfig():
    print(f'--------------------Start Django--------------------')
    print(f'--------------------Get Config--------------------')
    ALL_CONFIG_INFO = ConfManager.getInstance().get_flexconf_config()

    global CRON_CONFIG
    global DB_INFO

    CRON_CONFIG = ALL_CONFIG_INFO['CRON_CONFIG']
    DB_INFO = ConfManager.getInstance().getDbConfig()

    print('CRON_CONFIG = {}'.format(CRON_CONFIG))
    print('dbinfo = {}'.format(DB_INFO))


if __name__ == '__main__':
    print(f'ALMIF main() start')
    print(f'sys.argv len = [{len(sys.argv)}]')

    # set Process Name
    myProcName = 'ALMIF'

    if len(sys.argv) != 2:
        print(f"Error. Insufficient arguments")
        sys.exit()

    if sys.argv[1] != myProcName:
        print(f'Error. Invalid ProcName. ProcName=[{sys.argv[1]}]')
        sys.exit()

    print(f'***** OK...Start *****')
    print(f'********** Get Config ************')
    initConfig()

        


