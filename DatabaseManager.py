import configparser
import os
import sys
import json
import pymysql
import logging

# from .ConfigManager import ConfManager
from pymysql import MySQLError

class DbManager:

    def __init__(self, host, user, password, db, port=3306, charset='utf8'):
        # DB_INFO = ConfManager.getInstance().getDbConfig()
        self._logger = logging.getLogger(__name__)
        self._host = host  # DB_INFO['host']
        self._user = user  # DB_INFO['user']
        self._passwd = password  # DB_INFO['passwd']
        self._db = db  # DB_INFO['db']
        self._port = int(port)
        self._charset = charset
        try:
            self._connection = pymysql.connect(
            host=self._host,
            user=self._user,
            password=self._passwd,
            db=self._db,
            charset=self._charset
            )
        except MySQLError as error:
            print('Exception number: {}, value {!r}'.format(error.args[0], error))
            raise

    def select(self, sql_string):
        result = None

        try:
            # curs = self._connection.cursor()
            with self._connection as cursor:
                cursor.execute(sql_string)
                result = cursor.fetchall()

            return result
        except Exception as e:
            error_msg = str(e)
            #self._logger.debug('[select] error_msg = {}'.format(error_msg))
            print(f'[select] error_msg = [{error_msg}]')
            return result

    def insert(self, sql_string, raw_data=None):
        last_id = None

        try:
            curs = self._connection.cursor()

            if raw_data:
                curs.execute(query=sql_string, args=(raw_data))
            else:
                curs.execute(sql_string)

            last_id = self._connection.insert_id()
            self._connection.commit()

            return last_id

        except Exception as e:
            error_msg = str(e)
            #self._logger.debug('[insert] error_msg = {}'.format(error_msg))
            print(f'[insert] error_msg = [{error_msg}]')
            return last_id

    def update(self, sql_string, raw_data=None):
        result = None

        try:
            curs = self._connection.cursor()

            if raw_data:
                print('a')
                result = curs.execute(query=sql_string, args=(raw_data))
            else:
                result = curs.execute(sql_string)

            self._connection.commit()

            return result

        except Exception as e:
            error_msg = str(e)
            #self._logger.debug('[update] error_msg = {}'.format(error_msg))
            print(f'[update] error_msg = [{error_msg}]')
            return result

    def ping(self):
        self._connection.ping(reconnect=True)

    def _close(self):
        if getattr(self, '_connection', 0):
            try:
                return self._connection.close()
            except MySQLError as error:
                print("While closing connection ...")
                print('Exception number: {}, value {!r}'.format(error.args[0], error))
                raise

    def __del__(self):
        self._close()


if __name__ == '__main__':
    # example 1
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "PLTEIB"))
    # print(ConfManager.getInstance().getSysConfigData("MSGQUEUE_INFO", "proc2"))
    DB_INFO = {'host': '192.168.127.10', 'port': 3306, 'passwd': 'Dlxndl@123', 'user': 'e2e', 'db': 'e2edb'}
    # sql_string = 'select * from tb_e2eo_fc_workflow'
    sql_string = "UPDATE tb_e2eo_fc_workflow_result_raw SET bind_key='f2871f0a-9d40-4b09-bf25-deadcbad5f3d', exe_type='M', process_status='C', current_data=%s, group_date='2021-01-04 14:22:24' WHERE (workflow_id='be70c4c6-f06f-46bd-bd9f-fa57ceda31cd') and (workitem_id='5ee6c907-9609-46ae-a11b-627198b07d61') and (system_id='ISTB_7F_UPF01') and (requested_at='2021-01-04 14:22:24');"

    # UPDATE tb_e2eo_fc_workflow_result_raw SET bind_key='+'f2871f0a-9d40-4b09-bf25-deadcbad5f3d', exe_type='M', process_status='C', current_data=%s, group_date='2021-01-04 14:22:24' WHERE (workflow_id='be70c4c6-f06f-46bd-bd9f-fa57ceda31cd') and (workitem_id='5ee6c907-9609-46ae-a11b-627198b07d61') and (system_id='ISTB_7F_UPF01') and (requested_at='2021-01-04 14:22:24');
    # dbmanger = DbManager(DB_INFO)
    Dbmanager = DbManager('192.168.127.10','e2e','Dlxndl@123', 'e2edb')
    result = Dbmanager.insert(sql_string,'aaa')
    # result = DbManager().getInstance(DB_INFO).run_sql(sql_string)
    print(result)
