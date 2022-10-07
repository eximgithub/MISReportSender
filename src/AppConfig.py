class AppConfig:
    __seq: int = 0
    __oracle_database_connection: str
    __ott_wsdl_url: str
    __build_message_java_scripts: dict = {}
    __ready_flag_ora_script: str
    __get_report_data_ora_script: str
    __report_receiver_list_ora_script: str
    __message_templates: dict = {}
    __message_cached: dict = {}

    @staticmethod
    def get_seq():
        return AppConfig.__seq

    @staticmethod
    def set_seq(value):
        AppConfig.__seq = value

    @staticmethod
    def get_oracle_database_connection():
        return AppConfig.__oracle_database_connection

    @staticmethod
    def set_oracle_database_connection(value):
        AppConfig.__oracle_database_connection = value

    @staticmethod
    def get_ott_wsdl_url():
        return AppConfig.__ott_wsdl_url

    @staticmethod
    def set_ott_wsdl_url(value):
        AppConfig.__ott_wsdl_url = value

    @staticmethod
    def get_build_message_js(key):
        if AppConfig.__build_message_java_scripts.__contains__(key):
            return AppConfig.__build_message_java_scripts[key]
        return None

    @staticmethod
    def set_build_message_js(key, value):
        AppConfig.__build_message_java_scripts[key.upper()] = value
        print(AppConfig.__build_message_java_scripts)

    @staticmethod
    def get_ready_flag_ora_script():
        return AppConfig.__ready_flag_ora_script

    @staticmethod
    def set_ready_flag_ora_script(value):
        AppConfig.__ready_flag_ora_script = value

    @staticmethod
    def get_report_data_ora_script():
        return AppConfig.__get_report_data_ora_script

    @staticmethod
    def set_report_data_ora_script(value):
        AppConfig.__get_report_data_ora_script = value

    @staticmethod
    def get_report_receiver_list_ora_script():
        return AppConfig.__report_receiver_list_ora_script

    @staticmethod
    def set_report_receiver_list_ora_script(value):
        AppConfig.__report_receiver_list_ora_script = value

    @staticmethod
    def get_message_template(key):
        if AppConfig.__message_templates.__contains__(key):
            return AppConfig.__message_templates[key]
        return None

    @staticmethod
    def set_message_template(key, value):
        AppConfig.__message_templates[key.upper()] = value
        print(AppConfig.__message_templates)

    @staticmethod
    def get_message_cached(key):
        if AppConfig.__message_cached.__contains__(key):
            return AppConfig.__message_templates[key]
        return None

    @staticmethod
    def set_message_cached(key, value):
        AppConfig.__message_cached[key.upper()] = value
        print(AppConfig.__message_templates)
