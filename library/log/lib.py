import os
import logging
import traceback
from datetime import datetime
from logging.handlers import RotatingFileHandler

INFO = 'INFO'
ERROR = 'ERROR'
WARNING = 'WARNING'


class LoggerLib:
    default_path = os.path.join(
        os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))),
        'logs'
    )

    def __init__(self, name, max_bytes=10485760, backup_count=1):
        """Contructor class logger for directory and setting log files

        :param name : (String) log names
        :param max_bytes : (int) maximum size for logger files
        :param backup_count : (int) max backup files logger
        """
        self.check_directory(self.default_path)
        # self.date = DateClass()
        log_file = self.set_name(name.replace('.log', ''))
        self.logger = logging.getLogger(log_file)
        self.set_level(logging.INFO)
        self.logger.addHandler(self.set_handler(log_file, max_bytes, backup_count))

    @staticmethod
    def check_directory(path):
        """Check directory is exist, if directory is not exist service will make directory

        :return null"""

        try:
            os.makedirs(path)
        except OSError:
            if not os.path.isdir(path):
                raise

    def set_name(self, log_name):
        # self.date.get_date('full')
        return self.default_path + '/{}_{}.log'.format(
            log_name.replace('.log', ''), ''
        )

    def set_level(self, type_level):
        self.logger.setLevel(type_level)

    @staticmethod
    def set_handler(log_file, max_bytes, backup_count):
        return logging.handlers.RotatingFileHandler(
            log_file,
            maxBytes=max_bytes,
            backupCount=backup_count
        )

    @staticmethod
    def get_message(data):
        return "{0} [{1}] {2}".format(
            datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            data.get('method'),
            data.get('message')
        )

    def write_log(self, message, print_to_file=True, method=INFO, print_out=True):
        self.print_log(message, method) if print_out else None

        if print_to_file:
            result = {
                'INFO': lambda x: self.logger.info(self.get_message(x)),
                'ERROR': lambda x: self.logger.error(self.get_message(x)),
                'WARNING': lambda x: self.logger.warning(self.get_message(x)),
            }

            result.get(method, lambda x: str('Oops key is not found'))({
                'message': message,
                'method': method
            })

    def print_log(self, message, method=INFO):
        print(self.get_message({
            'message': message,
            'method': method
        }))
