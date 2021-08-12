# For SSH
import paramiko
import glob
import getpass
import time

# For Regular expression
import re

from datetime import datetime

# For other class or files
from almif_variables import *

from ConfigManager import ConfManager
from DatabaseManager import DbManager

DB_INFO = ConfManager.getInstance().getDbConfig()

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

    def __proc_alarm_db(self, alarm_data_list, latest_alarm_info):
        print(f'*********** __proc_alarm_db() Start! ***********')
        print(f'alarm_data_list len=[{len(alarm_data_list)}], latest_alarm_info=[{latest_alarm_info}]')

        Dbmanager = DbManager(DB_INFO['host'], DB_INFO['user'], DB_INFO['passwd'], DB_INFO['db'])

        sql_string = ''
        for idx, data in enumerate(alarm_data_list):
            # db_alarm_source = data['alarm_source']
            # db_alarm_time = data['alarm_time']
            # db_alarm_code = data['alarm_code']
            # db_alarm_name = data['alarm_name']
            # db_alarm_state = data['alarm_state']
            # db_ne_name = data['ne_name']
            # db_location = data['location']
            # db_event_type = data['event_type']
            # db_probable_cause = data['probable_cause']
            # db_specific_problem = data['specific_problem']
            # db_severity = data['severity']
            # db_additional_text = data['additional_text']
            # db_alarm_id = data['alarm_id']
            # db_notification_id = data['notification_id']
            # db_clear_user = data['clear_user']

            # print(f'================================================================')
            # print(f'idx=[{idx}] : alarm_source=[{db_alarm_source}], ' \
            #       f'alarm_time=[{db_alarm_time}], alarm_code=[{db_alarm_code}], ' \
            #       f'alarm_name=[{db_alarm_name}], alarm_state=[{db_alarm_state}], ' \
            #       f'ne_name=[{db_ne_name}], location=[{db_location}], ' \
            #       f'event_type=[{db_event_type}], probable_cause=[{db_probable_cause}], ' \
            #      f'specific_problem=[{db_specific_problem}], severity=[{db_severity}], ' \
            #      f'additional_text=[{db_additional_text}], alarm_id=[{db_alarm_id}], ' \
            #      f'notification_id=[{db_notification_id}], clear_user=[{db_clear_user}]')
            # print(f'================================================================')

            # select TB_E2EO_FC_FAULT_ALARM
            sql_string = "select alarm_time, alarm_state, severity from tb_e2eo_fc_fault_alarm " \
                         "WHERE vendor_type='" + self._vendor_type + "' " \
                         "AND rat_type='" + self._rat_type + "' " \
                         "AND alarm_code='" + data['alarm_code'] + "' " \
                         "AND location='" + data['location'] + "' "

            db_results = Dbmanager.select(sql_string)
            # print(f'sql_string=[\n{sql_string}\n]')
            # print(f'db_results=[\n{db_results}\n]')

            str_alarm_state = str(data['alarm_state'])
            alarm_state_type = DB_ALARM_STATE_CLEARED
            if str_alarm_state.upper() == 'OCCURRED':
                alarm_state_type = DB_ALARM_STATE_OCCURRED
            elif str_alarm_state.upper() == 'CLEARED':
                alarm_state_type = DB_ALARM_STATE_CLEARED
            else:
                print(f'unknown alarm_state. alarm_state=[{str_alarm_state}]')
                alarm_state_type = DB_ALARM_STATE_CLEARED

            if db_results != ():
                print(f'data is found at DB. Update tb_e2eo_fc_fault_alarm')
                # Update TB_E2EO_FC_FAULT_ALARM
                print(f'previous data : db_results=[{db_results}]')
                # Compare alarm time
                db_date_alarm_time = db_results[0][0]
                db_alarm_state = db_results[0][1]

                data_date_alarm_time = datetime.strptime(data['alarm_time'], "%Y-%m-%d %H:%M:%S.000")

                print(f'db data : db_date_alarm_time=[{db_date_alarm_time}], db_alarm_state=[{db_alarm_state}]')
                print(f'current data : data_date_alarm_time=[{data_date_alarm_time}], alarm_state_type=[{alarm_state_type}]')

                if (data_date_alarm_time <= db_date_alarm_time) and (alarm_state_type == db_alarm_state):
                    print(f'**** Same data and skip *****')
                    print(f'alarm time : current=[{data_date_alarm_time}], db=[{db_date_alarm_time}]')
                    print(f'alarm state : current=[{alarm_state_type}], db=[{db_alarm_state}]')
                    continue

                sql_string = "UPDATE tb_e2eo_fc_fault_alarm " \
                             "SET alarm_source='" + data['alarm_source'] + "', " \
                             "alarm_time='" + data['alarm_time'] + "', " \
                             "alarm_name='" + data['alarm_name'] + "', "\
                             "alarm_state='" + alarm_state_type + "', " \
                             "event_type='" + data['event_type'] + "', " \
                             "severity='" + data['severity'] + "', " \
                             "probable_cause='" + data['probable_cause'] + "', " \
                             "additional_text='" + data['additional_text'] + "', " \
                             "ne_type='" + data['ne_name'] + "', " \
                             "specific_problem='" + data['specific_problem'] + "', " \
                             "alarm_id='" + data['alarm_id'] + "', " \
                             "noti_id='" + data['notification_id'] + "', " \
                             "clear_user='" + data['clear_user'] + "', " \
                             "updated_at=NOW() " \
                             "WHERE vendor_type='" + self._vendor_type + "' " \
                             "AND rat_type='" + self._rat_type + "' " \
                             "AND alarm_code='" + data['alarm_code'] + "' " \
                             "AND location='" + data['location'] + "'; "
                Dbmanager.update(sql_string)
                # print(f'sql_string=[\n{sql_string}\n]')
            else: # if db_results != ():
                print(f'DB no data. Insert tb_e2eo_fc_fault_alarm')
                # Insert TB_E2EO_FC_FAULT_ALARM
                sql_string = "INSERT INTO tb_e2eo_fc_fault_alarm " \
                             "(vendor_type, rat_type, alarm_code, " \
                             "location, alarm_source, alarm_time, " \
                             "alarm_name, alarm_state, event_type, " \
                             "severity, probable_cause, additional_text, " \
                             "ne_type, specific_problem, alarm_id, " \
                             "noti_id, clear_user, updated_at) " \
                             "VALUES ('" + self._vendor_type + "', '" + self._rat_type + "', " \
                             "'" + data['alarm_code'] + "', '" + data['location'] + "', " \
                             "'" + data['alarm_source'] + "', '" + data['alarm_time'] + "', " \
                             "'" + data['alarm_name'] + "', '" + alarm_state_type + "', " \
                             "'" + data['event_type'] + "', '" + data['severity'] + "', " \
                             "'" + data['probable_cause'] + "', '" + data['additional_text'] + "', " \
                             "'" + data['ne_name'] + "', '" + data['specific_problem'] + "', " \
                             "'" + data['alarm_id'] + "', '" + data['notification_id'] + "', " \
                             "'" + data['clear_user'] + "', NOW());"
                Dbmanager.insert(sql_string)
                # print(f'sql_string=[\n{sql_string}\n]')

            # Insert TB_E2EO_FC_FAULT_ARLARM_HISTORY
            sql_string = "INSERT INTO tb_e2eo_fc_fault_alarm_history " \
                         "(vendor_type, rat_type, alarm_code, " \
                         "location, alarm_source, alarm_time, " \
                         "alarm_name, alarm_state, event_type, " \
                         "severity, probable_cause, additional_text, " \
                         "ne_type, specific_problem, alarm_id, " \
                         "noti_id, clear_user, updated_at) " \
                         "VALUES ('" + self._vendor_type + "', '" + self._rat_type + "', " \
                         "'" + data['alarm_code'] + "', '" + data['location'] + "', " \
                         "'" + data['alarm_source'] + "', '" + data['alarm_time'] + "', " \
                         "'" + data['alarm_name'] + "', '" + alarm_state_type + "', " \
                         "'" + data['event_type'] + "', '" + data['severity'] + "', " \
                         "'" + data['probable_cause'] + "', '" + data['additional_text'] + "', " \
                         "'" + data['ne_name'] + "', '" + data['specific_problem'] + "', " \
                         "'" + data['alarm_id'] + "', '" + data['notification_id'] + "', " \
                         "'" + data['clear_user'] + "', NOW());"

            Dbmanager.insert(sql_string)
            # print(f'sql_string=[\n{sql_string}\n]')

            # Update last alarm information to TB_E2EO_FC_ALARM_ACCESS_INFO
            sql_string = "UPDATE tb_e2eo_fc_alarm_access_info " \
                         "SET last_alarm_info='" + latest_alarm_info + "', " \
                         "access_at=NOW() " \
                         "WHERE name='" + self._name + "' " \
                         "AND connect_ip='" + self._conn_ip + "'; "
            Dbmanager.update(sql_string)
            # print(f'sql_string=[\n{sql_string}\n]')

        return True

    def __parse_5G_alarm(self, alarm_file):
        print(f'__parse_5G_alarm() Start!')
        if len(alarm_file) < 1:
            print(f'Error. Invalid File length. file len=[{len(alarm_file)}]')
            return False

        regex = re.compile(r'RANEMS\S+.*\n' \
                           r'\s[**|##].*\n' \
                           r'\s+NETWORKELEMENT.*\n' \
                           r'\s+LOCATION.*\n' \
                           r'\s+EVENTTYPE.*\n' \
                           r'\s+PROBABLECAUSE.*\n' \
                           r'\s+SPECIFICPROBLEM.*\n' \
                           r'\s+PERCEIVEDSEVERITY.*\n' \
                           r'\s+ADDITIONALTEXT.*\n' \
                           r'\s+COMPLETED.*\n' \
                           , re.MULTILINE)

        match_list = regex.findall(alarm_file)

        print(f'*** match_list type = [{type(match_list)}], match_list len=[{len(match_list)}] ***')
        print(f'***** Remove duplicated items ******')
        alarm_info_list = list()
        # Remove duplicated items
        for value in match_list:
            if value not in alarm_info_list:
                alarm_info_list.append(value)

        print(f'************************************')
        print(f'*** alarm_info_list type = [{type(alarm_info_list)}], alarm_info_list len=[{len(alarm_info_list)}] ***')

        # for sort.
        alarm_title_list = list()

        # alarm data list for database
        db_alarm_data_list = list()

        # variables for alarm data
        alarm_source = ''
        alarm_time = ''
        alarm_code = ''
        alarm_name = ''
        alarm_state = ''
        ne_name = ''
        location = ''
        event_type = ''
        probable_cause = ''
        specific_problem = ''
        severity = ''
        additional_text = ''

        # for Lte specific variables
        alarm_id = ''
        notification_id = ''
        clear_user = ''

        for idx, item in enumerate(alarm_info_list):
            alarm_item_str = ''.join(item)
            # print(f'idx=[{idx + 1}], alarm_item_str=[\n{alarm_item_str}]')
            split_str = alarm_item_str.split('\n')
            # print(f'idx=[{idx + 1}], type_split_str=[{type(split_str)}], split_str=[\n{split_str}]')
            for jdx, alarm_row in enumerate(split_str):
                # print(f'\n*** jdx=[{jdx+1}], alarm_row=[{alarm_row}] ***\n')
                if 'RANEMS' in alarm_row:
                    split_row = alarm_row.split(' ', maxsplit=1)
                    alarm_source = split_row[0]
                    alarm_time = split_row[1]

                    alarm_title_list.append(alarm_row)

                    # print(f'--- [RANEMS] : alarm_source=[{alarm_source}], alarm_time=[{alarm_time}] ---')

                elif '**' in alarm_row or '##' in alarm_row:
                    # print(f'--- [** or ##]=[{alarm_row}] ---')
                    split_row = alarm_row.split(' ')
                    split_row_len = len(split_row)
                    alarm_code = ''
                    alarm_name = ''
                    alarm_state = ''
                    for split_single_item in split_row:
                        if '**' in split_single_item or '##' in split_single_item:
                            continue
                        elif split_single_item.startswith('A') and split_single_item.isalpha() == False:
                            alarm_code = split_single_item
                        elif 'OCCURRED' in split_single_item or 'CLEARED' in split_single_item:
                            alarm_state = split_single_item
                        elif len(split_single_item) > 1:
                            alarm_name += split_single_item
                            alarm_name += ' '
                    # print(f'--- [**] : alarm_code=[{alarm_code}], alarm_name=[{alarm_name}],alarm_state=[{alarm_state}] ---')
                elif 'NETWORKELEMENT' in alarm_row:
                    # print(f'--- [NETWORKELEMENT]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    ne_name = split_row[1].lstrip().rstrip()
                    # print(f'--- [NETWORKELEMENT] : ne_name=[{ne_name}] ---')
                elif 'LOCATION' in alarm_row:
                    # print(f'--- [LOCATION]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    location = split_row[1].lstrip().rstrip()
                    # print(f'--- [LOCATION] : location=[{location}] ---')
                elif 'EVENTTYPE' in alarm_row:
                    # print(f'--- [EVENTTYPE]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    event_type = split_row[1].lstrip().rstrip()
                    # print(f'--- [EVENTTYPE] : event_type=[{event_type}] ---')
                elif 'PROBABLECAUSE' in alarm_row:
                    # print(f'--- [PROBABLECAUSE]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    probable_cause = split_row[1].lstrip().rstrip()
                    # print(f'--- [PROBABLECAUSE] : probable_cause=[{probable_cause}] ---')
                elif 'SPECIFICPROBLEM' in alarm_row:
                    # print(f'--- [SPECIFICPROBLEM]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    specific_problem = split_row[1].lstrip().rstrip()
                    # print(f'--- [SPECIFICPROBLEM] : specific_problem=[{specific_problem}] ---')
                elif 'PERCEIVEDSEVERITY' in alarm_row:
                    # print(f'--- [PERCEIVEDSEVERITY]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    severity = split_row[1].lstrip().rstrip()
                    # print(f'--- [PERCEIVEDSEVERITY] : severity=[{severity}] ---')
                elif 'ADDITIONALTEXT' in alarm_row:
                    # print(f'--- [ADDITIONALTEXT]=[{alarm_row}] ---')
                    split_row = alarm_row.split('=', maxsplit=1)
                    additional_text = split_row[1].lstrip().rstrip()
                    # print(f'--- [ADDITIONALTEXT] : additional_text=[{additional_text}] ---')
                elif 'COMPLETED' in alarm_row:
                    # print(f'--- [COMPLETED]=[{alarm_row}] ---')
                    # Set 5G Alarm dictionary
                    alarm_dict_5g = {'alarm_source':alarm_source,
                                    'alarm_time':alarm_time,
                                    'alarm_code':alarm_code,
                                    'alarm_name':alarm_name.rstrip().lstrip(),
                                    'alarm_state': alarm_state,
                                    'ne_name': ne_name,
                                    'location': location,
                                    'event_type': event_type,
                                    'probable_cause': probable_cause,
                                    'specific_problem': specific_problem,
                                    'severity': severity,
                                    'additional_text': additional_text,
                                    'alarm_id': '',
                                    'notification_id': '',
                                    'clear_user': ''}

                    db_alarm_data_list.append(alarm_dict_5g)

                else:
                    # print(f'--- [else]=[{alarm_row}] ---')
                    pass

        # Sort alarm time list. latest alarm time is first item.
        alarm_title_list.sort(key=lambda x: (x.split(' ')[1], x.split(' ')[2]), reverse=True)
        latest_alarm_info = alarm_title_list[0]

        print(f'\n************* Alarm Time Info Start *******************')
        print(f'alarm_title_list len=[{len(alarm_title_list)}]')

        for idx, item in enumerate(alarm_title_list):
            print(f'idx=[{idx + 1}] item=[{item}]')

        print(f'\nlatest_alarm_info=[{latest_alarm_info}]')
        print(f'************* Alarm Time Info End *******************\n')

        self.__proc_alarm_db(db_alarm_data_list, latest_alarm_info)

        return True

    def __parse_LTE_alarm(self, file):
        print(f'__parse_LTE_alarm() Start!')
        return True

    def get_remote_alarm(self):
        print(f'get_remote_alarm() Start!')

        # SSH connect
        self._cli.connect(self._conn_ip, port=self._conn_port,
                          username=self._user_id, password=self._user_pass)

        # process the remote file
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
                    self._cli.close()
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
                if self._rat_type == RAT_TYPE_5G:
                    print(f'*** RAT_TYPE_5G ***')
                    ret = self.__parse_5G_alarm(alarm_file)
                    if ret != True:
                        print(f'Error. __parse_5G_alarm() fail')
                        self._cli.close()
                        return False

                elif self._rat_type == RAT_TYPE_LTE:
                    print(f'*** RAT_TYPE_LTE ***')
                    ret = self.__parse_LTE_alarm(alarm_file)
                    if ret != True:
                        print(f'Error. __parse_LTE_alarm() fail')
                        self._cli.close()
                        return False
                else:
                    print(f'*** Unknown RAT_TYPE ***, rat_type=[{self._rat_type}]')
                    self._cli.close()
                    return False


        self._cli.close()
        return True

    def print_access_info(self):
        print(f'name=[{self._name}], conn_ip=[{self._conn_ip}], conn_port=[{self._conn_port}], ' \
              f'user_id=[{self._user_id}], user_pass=[{self._user_pass}], ' \
              f'vendor_type=[{self._vendor_type}], rat_type=[{self._rat_type}], ' \
              f'file_path=[{self._file_path}], last_alarm_info=[{self._last_alarm_info}]')