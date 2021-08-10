# For SSH
import paramiko
import glob
import getpass
import time

class AlarmMgr:
    def __init__(self, access_info, charset='utf8'):
        if len(access_info) < 1:
            return None

        # Create SSH Client
        self._cli = paramiko.SSHClient()
        self._cli.set_missing_host_key_policy(paramiko.AutoAddPolicy)

        # Save access information to self variables.
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

        # private variables


        # check validation
        if len(self._conn_ip) < 1 or len(self._conn_port) < 1:
            print(f'Error. Invalid connection info. conn_ip=[{self._conn_ip}], conn_port=[{self._conn_port}]')
            return None

        if len(self._user_id) < 1 or len(self._user_pass) < 1:
            print(f'Error. Invalid access info. user_id=[{self._user_id}], user_pass=[{self._user_pass}]')
            return None

        if len(self._vendor_type) < 1 or len(self._rat_type) < 1:
            print(f'Error. Invalid vendor info. vendor_type=[{self._vendor_type}], rat_type=[{self._rat_type}]')
            return None

        if len(self._file_path) < 1:
            print(f'Error. Invalid file info. file_path=[{self._file_path}]')
            return None

    def __bytes_to_string(self, byte_or_int_value, encoding='utf-8'):
        if isinstance(byte_or_int_value, bytes):
            return byte_or_int_value.decode(encoding)
        if isinstance(byte_or_int_value, int):
            return chr(byte_or_int_value).encode(encoding).decode(encoding)
        else:
            print(f'Error: Input must be a bytes or int type')
            return None

    def __parse_5G_alarm(self, file):
        return True

    def __parse_LTE_alarm(self, file):
        return True

    def get_remote_alarm(self):
        print(f'get_remote_alarm() Start!')

        # SSH connect
        self._cli.connect(self._conn_ip, port=self._conn_port,
                          username=self._user_id, password=self._user_pass)

        # parsing the remote file
        with self._cli.open_sftp() as sftp_client:
            with sftp_client.open(self._file_path, 'r') as remote_file:
                print(f'remote file open success! filename=[{self._file_path}]')

                # Calling SFTPFile.prefetch should increase the read speed
                remote_file.prefetch()
                binary_data = remote_file.read()
                print(f'binary_data type=[{type(binary_data)}], binary_data len=[{len(binary_data)}]')

                text_data = self.__bytes_to_string(binary_data)
                if text_data == None:
                    print(f'Error. __bytes_to_string() fail')
                    return False

                print(f'text_data type=[{type(text_data)}], text_data len=[{len(text_data)}]')

                ##### search location of last alarm #####
                search_loc = None
                alarm_file = None
                if len(self._last_alarm_info) < 1:
                    print(f'last_alarm_info is empty')
                    alarm_file = text_data[:]
                else:
                    print(f'last_alarm_info is NOT empty. last_alarm_info=[{self._last_alarm_info}]')
                    search_loc = text_data.find(self._last_alarm_info)
                    print(f'search_loc type=[{type(search_loc)}], search_loc=[{search_loc}]')
                    if search_loc > 0:
                        print(f'last alarm info search success! search_loc=[{search_loc}]]')
                        #### slicing alarm information #####
                        alarm_file = text_data[(search_loc):]
                    else:
                        print(f'Error. last alarm info search fail! search_loc=[{search_loc}]]')
                        alarm_file = text_data[:]

                print(f'alarm_file type=[{type(alarm_file)}], alarm_file len=[{len(alarm_file)}]')

        self._cli.close()
        return True

    def print_access_info(self):
        print(f'name=[{self._name}], conn_ip=[{self._conn_ip}], conn_port=[{self._conn_port}], ' \
              f'user_id=[{self._user_id}], user_pass=[{self._user_pass}], ' \
              f'vendor_type=[{self._vendor_type}], rat_type=[{self._rat_type}], ' \
              f'file_path=[{self._file_path}], last_alarm_info=[{self._last_alarm_info}]')