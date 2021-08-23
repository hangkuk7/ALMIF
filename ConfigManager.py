import configparser
import os
import sys
import json


class ConfManager:

    LOG_INFO = "LOG_INFO"
    SYS_CONFIG_GENERAL = "GENERAL"

    CONFIG_PATH = os.environ.get('HOME', '') + '/data/CONFIG/ALMIF.dat'

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
            print("Error. Exception. Please set the environment variable HOME")

        # MY_SYS_NAME
        try:
            self.sys_name_str = os.environ["MY_SYS_NAME"]
            print("MY_SYS_NAME : " + str(self.sys_name_str))

        except KeyError:
            self.sys_name_str = ""
            print("'Error. Exception. Please set the environment variable MY_SYS_NAME")

        # HOSTNAME
        try:
            self.host_name = os.environ['HOSTNAME']
            print("HOSTNAME : " + str(self.host_name))
        except KeyError:
            self.host_name = 'E2E-O'
            print("'Error. Exception. Please set the environment variable HOSTNAME")

        self.sysConfig = configparser.ConfigParser()
        self.sysConfig.read(self.home_str + '/data/sysconfig', encoding='euc-kr')

        for each_section in self.sysConfig.sections():
            dictionary = dict()
            for (each_key, each_val) in self.sysConfig.items(each_section):
                dictionary[each_key] = each_val

            # append(index, value)
            self.sysdictList[each_section] = dictionary

        #############################################################################
        # [1] Load SYSCONFIG
        try:
            # SYSCONFIG
            self.db_user = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_ID", 1))
            self.db_passwd = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_PW", 1))
            self.db_port = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_PORT", 1))
            self.db_name = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_NAME", 1))
            self.db_host = str(self.getSysConfigData(ConfManager.SYS_CONFIG_GENERAL, "DB_IPADDR", 1))

        except Exception as errmsg:
            print('Error. Exception in read SYSCONFIG config : {}'.format(errmsg))
        #############################################################################

        #############################################################################
        # [2] FILE READ LOCAL CONFIG
        self.localConfig = configparser.ConfigParser()
        # self.localConfig.read('ALMIF.dat')
        self.localConfig.read(self.home_str + '/data/CONFIG/ALMIF.dat', encoding='euc-kr')
        local_config_section = self.localConfig.sections()

        for each_section in self.localConfig.sections():
            dictionary = dict()
            for (each_key, each_val) in self.localConfig.items(each_section):
                dictionary[each_key] = each_val

            # append(index, value)
            self.localdictList[each_section] = dictionary

        # Load LocalConfig
        try:
            # [GENERAL] section
            self.err_log_level = self.getLocalConfigData("GENERAL", "ERR_LOG_LEVEL", 1)
            self.msg_log_level = self.getLocalConfigData("GENERAL", "MSG_LOG_LEVEL", 1)

            # [TIME_CONFIG] section
            self.time_interval = self.getLocalConfigData("TIME_CONFIG", "TIME_INTERVAL", 1)

        except Exception as errmsg:
            print('Error. Exception in read LocalConfig config : {}'.format(errmsg))

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

    # def getLocalConfigData(self, section, confKey):
    #
    #     for key in self.localdictList.keys():
    #         print (key)
    #         if key.upper() != section.upper():
    #             continue
    #
    #         for instance in self.localdictList[key].keys():
    #             if instance.upper() != confKey.upper():
    #                 continue
    #
    #             return self.localdictList[key][instance]
    #
    #     print("Local Conf - Can't not found SECTION[%s] KEY[%s] " % (section, confKey))
    #     return None
    def getLocalConfigData(self, section, confKey, offset=0):

        for key in self.localdictList.keys():
            print (key)
            if key.upper() != section.upper():
                continue

            for instance in self.localdictList[key].keys():
                if instance.upper() != confKey.upper():
                    continue

                val = self.localdictList[key][instance]

            if offset == 0:
                return val
            else:

                idx = 1
                vList = val.split()
                for v in vList:
                    if offset == idx:
                        return v
                    idx = idx + 1

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

        return dbInfo

    def getLocalConfig(self):

        localConfigInfo = {}
        # [GENERAL] section
        localConfigInfo['err_log_level'] = self.err_log_level
        localConfigInfo['msg_log_level'] = self.msg_log_level

        # [TIME_CONFIG] section
        localConfigInfo['time_interval'] = self.time_interval

        return localConfigInfo

    # def get_config_data(self):
    #     parser = configparser.ConfigParser()
    #     parser.read(ConfManager.CONFIG_PATH)
    #
    #     ALL_CONFIG_INFO = {}
    #
    #     CRON_CONFIG = {}
    #     TIME_CONFIG = {}
    #
    #     CRON_KEY = ['CRON_FILE_PATH', 'CRON_LOG_PATH', 'CRON_USER']
    #     TIME_KEY = ['TIME_INTERVAL']
    #
    #     raw = 'CRON_CONFIG'
    #     for k in CRON_KEY:
    #         CRON_CONFIG[k] = parser.get(raw, k)
    #
    #     raw = 'TIME_CONFIG'
    #     for k in TIME_KEY:
    #         TIME_CONFIG[k] = parser.get(raw, k)
    #
    #     ALL_CONFIG_INFO['CRON_CONFIG'] = CRON_CONFIG
    #     ALL_CONFIG_INFO['TIME_CONFIG'] = TIME_CONFIG
    #
    #     return ALL_CONFIG_INFO

if __name__ == '__main__':
    pass
    # example 1
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "PLTEIB"))
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "proc2"))
    # ALL_CONFIG_INFO = ConfManager.getInstance().get_config_data()
    # print(ALL_CONFIG_INFO)
    # print(ALL_CONFIG_INFO['CRON_CONFIG'])



