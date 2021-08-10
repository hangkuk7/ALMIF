

class AlarmMgr:
    def __init__(self, access_info, charset='utf8'):
        if len(access_info) < 1:
            return None

        self._name = access_info[0]
        self._conn_ip = access_info[1]
        self._conn_port = access_info[2]
        self._user_id = access_info[3]
        self._user_pass = access_info[4]
        self._vendor_type = access_info[5]
        self._rat_type = access_info[6]
        self._file_path = access_info[7]
        self._last_alarm_info = access_info[8]
        self._access_at = access_info[9]

        # validate cheack
        if len(self._conn_ip) < 1 or len(self._conn_port) < 1:
            print('Error. Invalid connection info. conn_ip=[{self._conn_ip}], conn_port=[{self._conn_port}]')
            return None

        if len(self._user_id) < 1 or len(self._user_pass):
            print('Error. Invalid access info. user_id=[{self._user_id}], user_pass=[{self._user_pass}]')
            return None

        if len(self._vendor_type) < 1 or len(self._rat_type):
            print('Error. Invalid vendor info. vendor_type=[{self._vendor_type}], rat_type=[{self._rat_type}]')
            return None

        if len(self._file_path):
            print('Error. Invalid file info. file_path=[{self._file_path}]')
            return None

    def print_access_info(self):
        print(f'name=[{self._name}], conn_ip=[{self._conn_ip}], conn_port=[{self._conn_port}' \
              f'user_id=[{self._user_id}], user_pass=[{self._user_pass}], ' \
              f'vendor_type=[{self._vendor_type}], rat_type=[{self._rat_type}], ' \
              f'file_path=[{self._file_path}], last_alarm_info=[{self._last_alarm_info}]')