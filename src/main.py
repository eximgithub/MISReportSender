import os
import uuid
import logging.config
from datetime import datetime, timedelta
import configparser
import js2py
import schedule
import time

from base.utils.oracle.executor import get_data_from_db
from AppConfig import AppConfig as appConfig
from base.serialization.XMLSerializer import XMLSerializer
from base.utils.soap.OTTUtil import OTTRequest, OTTResponse
from base.utils.soap.OTTUtil import send as ott_send

CONFIG_FILE_NAME: str = "../config.conf"
OTT_MESSAGE_TYPE: str = "3"
DATE_FORMAT: str = '%Y%m%d'
DATETIME_FORMAT: str = "%m/%d/%Y, %H:%M:%S"


def get_data_ready_flag():
    try:
        with open(f"../scripts/oracle/get_ready_flag_ora_script.sql") as f:
            __get_ready_flag_ora_script = f.read()

        if get_data_from_db(appConfig.get_oracle_database_connection(), __get_ready_flag_ora_script)[0][0] == 1:
            return True
        else:
            logger.info("Data is not ready!")
            return False
    except Exception as ex:
        logger(f"Error: {str(ex)}")
        return False


def build_ott_message(message_type, send_to):
    try:
        message_key = f"{message_type}_{send_to}"
        if appConfig.get_message_cached(message_key) is None:
            print(f"Position: {send_to}")
            report_data = get_data_from_db(appConfig.get_oracle_database_connection(),
                                           appConfig.get_report_data_ora_script())
            message_template = appConfig.get_message_template(send_to)
            print(f"Message Template: {message_template}")
            javascript = appConfig.get_build_message_js(send_to)
            if javascript is not None:
                func = js2py.eval_js(javascript)
                print(f"javascript: {javascript}")
                message = func(message_template, report_data)
            else:
                message = message_template
            appConfig.set_message_cached(message_key, message)
        else:
            message = appConfig.get_message_cached(message_key)
            print("Loaded message from cacher")
        return message
    except Exception as ex:
        logger(f"Error: {str(ex)}")
        return None


def build_ott_request(cif, mobile, message):
    request = OTTRequest()
    request.type = OTT_MESSAGE_TYPE
    request.content = message
    request.mobile = mobile
    request.cif = cif
    request.messageId = str(uuid.uuid4())
    request.priority = "2"
    request.mediaUrl = ""
    request.mediaType = ""
    request.expireTime = ""
    request.messageTime = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request.isEncrypt = "0"
    return request


def get_phone_number_list():
    return get_data_from_db(appConfig.get_oracle_database_connection(), appConfig.get_report_receiver_list_ora_script())


def send_ott_by_list():
    print(f"Run at: {datetime.today().strftime(DATETIME_FORMAT)}")
    print(f"Application sequence: {appConfig.get_seq()}")
    print(f"Current date: {int(datetime.today().strftime(DATE_FORMAT))}")

    if appConfig.get_seq() < int(datetime.today().strftime(DATE_FORMAT)) or True:
        if get_data_ready_flag():
            next_date_as_int = int((datetime.today() + timedelta(days=1)).strftime(DATE_FORMAT))
            print(f"Next date: {next_date_as_int}")
            appConfig.set_seq(next_date_as_int)
            phone_number_list = get_phone_number_list()
            for x in phone_number_list:
                try:
                    cif = x[0]
                    mobile = x[1]
                    position = x[2]
                    message_type = "ReportType"
                    message = build_ott_message(message_type, position)
                    request = build_ott_request(cif, mobile, message)
                    logger.info(XMLSerializer.Serialize(request).encode('utf8'))
                    response = ott_send(appConfig.get_ott_wsdl_url(), request)
                    logger.info(XMLSerializer.Serialize(response).encode('utf8'))
                except Exception as ex:
                    logger.exception(ex)


def get_default_config(key: str):
    try:
        return config['DEFAULT'][key]
    except Exception as ex:
        logger.error(f"Key {key} is not constant on default config")
        logger.exception(ex)


if __name__ == '__main__':
    print(os.getcwd())
    # load logging config
    logging.config.fileConfig(CONFIG_FILE_NAME)
    # create logger
    logger = logging.getLogger(__name__)

    config = configparser.ConfigParser()
    config.read(CONFIG_FILE_NAME)

    # load oracle database config
    host = config['oracle_database']['host']
    port = config['oracle_database']['port']
    sid = config['oracle_database']['sid']
    user = config['oracle_database']['user']
    passwd = config['oracle_database']['passwd']
    appConfig.set_oracle_database_connection(f"{user}/{passwd}@//{host}:{port}/{sid}")
    appConfig.set_ott_wsdl_url(config['DEFAULT']['ott_wsdl_url'])

    # load script config

    with open(f"../scripts/oracle/get_ready_flag_ora_script.sql") as f:
        appConfig.set_ready_flag_ora_script(f.read())

    with open(f"../scripts/oracle/get_report_data_ora_script.sql") as f:
        appConfig.set_report_data_ora_script(f.read())

    with open(f"../scripts/oracle/get_report_receiver_list_ora_script.sql") as f:
        appConfig.set_report_receiver_list_ora_script(f.read())

    # init build message javascript
    if get_default_config('javascript_directory') is None:
        javascript_directory = f"{os.getcwd()}/../scripts/js"
    else:
        javascript_directory = get_default_config('javascript_directory')

    for directory, subdirectories, files in os.walk(javascript_directory):
        for file in files:
            if file.__contains__(".build_message.js"):
                key = file.replace(".build_message.js", "")
                with open(f"{javascript_directory}/{file}", encoding="utf8") as f:
                    val = f.read()
                appConfig.set_build_message_js(key, val)

    # init message templates
    if get_default_config('template_directory') is None:
        template_directory = f"{os.getcwd()}/../templates"
    else:
        template_directory = get_default_config('template_directory')
    for directory, subdirectories, files in os.walk(template_directory):
        for file in files:
            if file.__contains__(".template.txt"):
                key = file.replace(".template.txt", "")
                with open(f"{template_directory}/{file}") as f:
                    val = f.read().replace("\n", "\r\n")
                appConfig.set_message_template(key, val)

    run_at = config['DEFAULT']['run_at']
    logger.info(f"run_at: {run_at}")

    process_sleep_time = config['DEFAULT']['process_sleep_time']
    logger.info(f"process_sleep_time: {process_sleep_time}")

    send_ott_by_list()
    # send_ott_by_list();
    # def create_day_schedule(at_time):
    #     print(f"at_time: {at_time}")
    #     schedule.every().day.at(at_time).do(send_ott_by_list)
    #
    #
    # for at_time in run_at.split("|"):
    #     # eval(f"create_day_schedule('{at_time}')")
    #     eval(f"schedule.every().day.at('{at_time}').do(send_ott_by_list)")
    #
    # while True:
    #     schedule.run_pending()
    #     time.sleep(int(process_sleep_time))
