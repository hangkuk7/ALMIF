import configparser
import os
import sys
import json

from LogManager import LogManager

# For log
logger = LogManager.getInstance().get_logger()

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
            logger.info("HOME : " + str(self.home_str))
        except KeyError:
            logger.critical("Error. Exception. Please set the environment variable HOME")

        # MY_SYS_NAME
        try:
            self.sys_name_str = os.environ["MY_SYS_NAME"]
            logger.info("MY_SYS_NAME : " + str(self.sys_name_str))

        except KeyError:
            self.sys_name_str = ""
            logger.critical("'Error. Exception. Please set the environment variable MY_SYS_NAME")

        # HOSTNAME
        try:
            self.host_name = os.environ['HOSTNAME']
            logger.info("HOSTNAME : " + str(self.host_name))
        except KeyError:
            self.host_name = 'E2E-O'
            logger.critical("'Error. Exception. Please set the environment variable HOSTNAME")

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
            logger.critical('Error. Exception in read SYSCONFIG config : {}'.format(errmsg))
        #############################################################################

        #############################################################################
        # [2] FILE READ LOCAL CONFIG
        self.localConfig = configparser.ConfigParser()
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
            self.msg_log_level = int(self.getLocalConfigData("GENERAL", "MSG_LOG_LEVEL", 1))
            if self.msg_log_level < 1 or self.msg_log_level >= 5:
                logger.warnning(f'Invalid mag_log_level=[{self.msg_log_level}]')
                self.msg_log_level = 5

            # [TIME_CONFIG] section
            self.time_interval = int(self.getLocalConfigData("TIME_CONFIG", "TIME_INTERVAL", 1))

        except Exception as errmsg:
            logger.critical('Error. Exception in read LocalConfig config : {}'.format(errmsg))

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

        logger.critical("[getSysConfigData] -Can't not found SECTION[%s] KEY[%s] " % (section, confKey))
        return None

    def getLocalConfigData(self, section, confKey, offset=0):

        for key in self.localdictList.keys():
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

        logger.critical("[getLocalConfigData] Can't not found SECTION[%s] KEY[%s] " % (section, confKey))
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
        localConfigInfo['msg_log_level'] = self.msg_log_level

        # [TIME_CONFIG] section
        localConfigInfo['time_interval'] = self.time_interval

        return localConfigInfo

if __name__ == '__main__':
    pass
    # example 1
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "PLTEIB"))
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "proc2"))
    # ALL_CONFIG_INFO = ConfManager.getInstance().get_config_data()
    # print(ALL_CONFIG_INFO)
    # print(ALL_CONFIG_INFO['CRON_CONFIG'])



