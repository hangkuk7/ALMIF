import configparser
import os
import sys
import json


class ConfManager:

    LOG_INFO = "LOG_INFO"
    SYS_CONFIG_GENERAL = "GENERAL"

    # edited by hangkuk at 2021.06.15 
    FLEXCONF_CONFIG_PATH = os.environ.get('HOME', '') + '/data/CONFIG/FCENGINE.dat'
    #FLEXCONF_CONFIG_PATH = '/data1/e2e/data/CONFIG/FCENGINE.dat'
    #FLEXCONF_CONFIG_PATH = 'FCENGINE.dat'

    __instance = None
    sysdictList = dict()
    localdictList = dict()

    @staticmethod
    def getInstance():
        """ Static access method. """
        if ConfManager.__instance == None:
            ConfManager.__instance = ConfManager()
        return ConfManager.__instance

    def __init__(self):
         self.initConfFile()

    def initConfFile(self):

        #############################################################################
        # [1] FILE READ SYSCONFIG
        try:
            self.home_str = os.environ["HOME"]
            print("HOME : " + str(self.home_str))
        except KeyError:
            print("Please set the environment variable HOME")
            sys.exit(1)

        self.sysConfig = configparser.ConfigParser()
        self.sysConfig.read(self.home_str + '/data/sysconfig', encoding='euc-kr')

        for each_section in self.sysConfig.sections():
            dictionary = dict()
            for (each_key, each_val) in self.sysConfig.items(each_section):
                dictionary[each_key] = each_val

            # append(index, value)
            self.sysdictList[each_section] = dictionary

        try:
            self.sys_name_str = os.environ["MY_SYS_NAME"]
            print("HOME : " + str(self.sys_name_str))

        except KeyError:
            self.sys_name_str = ""
            print("Please set the environment variable MY_SYS_NAME")

        #############################################################################
        # [2] FILE READ LOCAL CONFIG
        self.localConfig = configparser.ConfigParser()
        self.localConfig.read('FCENGINE.dat')

        for each_section in self.localConfig.sections():
            dictionary = dict()
            for (each_key, each_val) in self.localConfig.items(each_section):
                dictionary[each_key] = each_val

            # append(index, value)
            self.localdictList[each_section] = dictionary

        # [3] LOG INFO
        # self.logFlag = self.getLocalConfigData("LOG_INFO", "LOG_FLAG")
        # self.logLevel = int(self.getLocalConfigData("LOG_INFO", "LOG_LEVEL"))
        # self.logFlag = self.logFlag.upper()
        self.msglogFile = str(self.getLocalConfigData("LOG_INFO", "MSG_LOG_FILE"))
        self.errlogFile = str(self.getLocalConfigData("LOG_INFO", "ERR_LOG_FILE"))
        # self.logMaxSize = int(self.getLocalConfigData("LOG_INFO", "LOG_MAX_SIZE"))
        # self.maxBackupCnt = int(self.getLocalConfigData("LOG_INFO", "MAX_FILE_BKUP_COUNT"))


        try:

            self.db_user = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_ID", 1))
            self.db_passwd = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_PW", 1))
            self.db_port = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_PORT", 1))
            self.db_name = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_NAME", 1))
            self.db_host = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_IPADDR", 1))

        except Exception as errmsg:
            print('Exception in read config : {}'.format(errmsg))
            # from ExceptionHandler import ExceptionManager
            # ExceptionManager.process_stop()

        try:
            self.host_name = os.environ['HOSTNAME']
        except KeyError:
            self.host_name = 'E2E-O'
        #############################################################################

    def getSysConfigData(self, section, confKey, offset=0):

        for key in self.sysdictList.keys():
            if key.upper() != section.upper():
                continue

            for instance in self.sysdictList[key].keys():
                if instance.upper() != confKey.upper():
                    continue

                val = self.sysdictList[key][instance]

                if offset == 0:
                    return val
                else:

                    idx = 1
                    vList = val.split()
                    for v in vList:
                        if offset == idx:
                            return v
                        idx = idx + 1

        print("Sys Conf -Can't not found SECTION[%s] KEY[%s] " % (section, confKey))
        return None

    def getLocalConfigData(self, section, confKey):

        for key in self.localdictList.keys():
            print (key)
            if key.upper() != section.upper():
                continue

            for instance in self.localdictList[key].keys():
                if instance.upper() != confKey.upper():
                    continue

                return self.localdictList[key][instance]

        print("Local Conf - Can't not found SECTION[%s] KEY[%s] " % (section, confKey))
        return None

    def getDbConfig(self):

        # MYSQL
        dbInfo = {}
        dbInfo['host'] = self.db_host
        dbInfo['port'] = int(self.db_port)
        dbInfo['passwd'] = self.db_passwd
        dbInfo['user'] = self.db_user
        dbInfo['db'] = self.db_name

        '''
        # POSTGRE SQL
        dbInfo = {}
        dbInfo['host'] = self.db_host
        dbInfo['port'] = self.db_port
        dbInfo['password'] = self.db_passwd
        dbInfo['user'] = self.db_user
        dbInfo['database'] = self.db_name
        '''

        return dbInfo

    def get_flexconf_config(self):
        parser = configparser.ConfigParser()
        parser.read(ConfManager.FLEXCONF_CONFIG_PATH)

        ALL_CONFIG_INFO = {}

        CRON_CONFIG = {}
        WORKFLOW_CONFIG = {}
        WORKITEM_CONFIG = {}
        ENGINE_API_CONFIG = {}
        TOMCAT_API_CONFIG = {}

        CRON_KEY = ['CRON_FILE_PATH', 'CRON_LOG_PATH', 'CRON_USER']
        WORKFLOW_KEY = ['WORKFLOW_PATH']
        WORKITEM_KEY = ['WORKITEM_PATH']
        ENGINE_API_KEY = ['ENGINE_VIP_URI']
        TOMCAT_API_KEY = ['TOMCAT_VIP_URI']

        raw = 'CRON_CONFIG'
        for k in CRON_KEY:
            CRON_CONFIG[k] = parser.get(raw, k)

        raw = 'WORKFLOW_CONFIG'
        for k in WORKFLOW_KEY:
            WORKFLOW_CONFIG[k] = parser.get(raw, k)

        raw = 'WORKITEM_CONFIG'
        for k in WORKITEM_KEY:
            WORKITEM_CONFIG[k] = parser.get(raw, k)

        raw = 'ENGINE_API_CONFIG'
        for k in ENGINE_API_KEY:
            ENGINE_API_CONFIG[k] = parser.get(raw, k)

        raw = 'TOMCAT_API_CONFIG'
        for k in TOMCAT_API_KEY:
            TOMCAT_API_CONFIG[k] = parser.get(raw, k)

        ALL_CONFIG_INFO['CRON_CONFIG'] = CRON_CONFIG
        ALL_CONFIG_INFO['WORKFLOW_CONFIG'] = WORKFLOW_CONFIG
        ALL_CONFIG_INFO['WORKITEM_CONFIG'] = WORKITEM_CONFIG
        ALL_CONFIG_INFO['ENGINE_API_CONFIG'] = ENGINE_API_CONFIG
        ALL_CONFIG_INFO['TOMCAT_API_CONFIG'] = TOMCAT_API_CONFIG

        return ALL_CONFIG_INFO

if __name__ == '__main__':
    # example 1
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "PLTEIB"))
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "proc2"))
    ALL_CONFIG_INFO = ConfManager.getInstance().get_flexconf_config()
    print(ALL_CONFIG_INFO)
    print(ALL_CONFIG_INFO['CRON_CONFIG'])

