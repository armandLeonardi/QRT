import datetime
import json
import os
import base64

class Core:

    def __init__(self, path_config: str = "" ,datetime_format: str = "%d/%m/%y %H:%M:%S", encoding_format: str = "utf8", cls: str = "Core", verbose: bool = True, debug: bool = True, formated: bool = True, *args, **kargs):
        self.__version__ = "1.0.0"
        self._messages_codes = {10: 'debug', 20: 'info', 30: 'warning', 40: 'error'}
        self.cls = cls
        self._verbose = verbose
        self._debug = debug
        self.formated = formated
        self.datetime_format = datetime_format
        self.encoding_format = encoding_format
        self.path_config = path_config
        self.path_log_folder = ""
        self.filename_log = ""
        self.logger = None
        self.logger_open = False

    def now(self, datetime_format: str = ""):
        datetime_format = datetime_format if datetime_format != "" else self.datetime_format
        return datetime.datetime.now().strftime(datetime_format)  

    def load_config(self):

        config = {}

        if self.path_config == "":
            raise ValueError("Confguration path is empty")
        else:
            with open(self.path_config, 'r', encoding=self.encoding_format) as f:
                config = json.load(f)
                f.close()

                for key, value in config.items():
                    if key in self.__dict__:
                        self.__setattr__(key, value)

    def _format_message(self, message_type: str, message: str):
        formated_message = f"{self.now()} | {self.cls: <9} | {message_type: <9} | {message}"
        return formated_message
    
    def _display(self, message: str, end: str = "\n"):

        print(message, end=end)

    def open_log_file(self):

        if self.path_log_folder != "":
            _now = self.now(datetime_format="%d%m%y%H%M%S")
            log_filename = f"{_now}_{self.cls}.log"

            full_path_log_filename = os.path.join(self.path_log_folder, log_filename)
            self.filename_log = full_path_log_filename

            self.logger = open(full_path_log_filename, 'a', encoding=self.encoding_format)
            self.logger_open = True

        else:
            self.warning("Log folder path is empty")

    def set_logger(self, other):

        if 'logger' in other.__dict__:
            if other.logger is not None:
                self.logger = other.logger
                self.logger_open = True

    def write_log(self, message: str, end: str = "\n"):

        if self.logger_open is True:
            try:
                self.logger.write(f"{message}{end}")
                self.logger.flush()
            except Exception as error:
                self.error(error)

    def close_log(self):

        try:
            self.logger.close()
            self.logger_open = False
            self.info(f"Closing log folder {self.filename_log}")
        except Exception as error:
            self.error(error)

    def debug(self, message: str = "[default debug message]"):

        _message = ""
        if self.formated is True:
            _message = self._format_message('debug', message)
        else:
            _message = message

        if self._debug is True:
            self._display(_message)

        self.write_log(_message)

    def info(self, message: str = "[default info message]"):        

        _message = ""
        if self.formated is True:
            _message = self._format_message('info', message)
        else:
            _message = message

        if self._verbose is True:
            self._display(_message)

        self.write_log(_message)

    def warning(self, message: str = "[default warning message]"):        

        _message = ""
        if self.formated is True:
            _message = self._format_message('warning', message)
        else:
            _message = message

        self.write_log(_message)
        self._display(_message)
        
    def error(self, message: str = "[default error message]"):        

        _message = ""
        if self.formated is True:
            _message = self._format_message('error', message)
        else:
            _message = message

        self.write_log(_message)
        self._display(_message)


class Base64Engine:

    encoding = "utf8"

    @classmethod
    def encode(cls, chars: str):
        chars = str(chars)
        return base64.b64encode(chars.encode(encoding=Base64Engine.encoding)).decode(encoding=Base64Engine.encoding)
    
    @classmethod
    def decode(cls, chars64: str):
        return base64.b64decode(chars64).decode(encoding=Base64Engine.encoding)


if __name__ == "__main__":

    c = Core(path_config=r"D:\Informatique\QRT\demo_core_config.json")

    c.load_config()

    c.debug("my debug message")
    c.info("my info message")
    c.warning("my warning message")
    c.error("my error message")

    c.open_log_file()
 
    c.debug("my debug message")
    c.info("my info message")
    c.warning("my warning message")
    c.error("my error message")

    c.close_log()
