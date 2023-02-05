import datetime
import json

class Core:

    def __init__(self, path_config: str = "" ,datetime_format: str = "d%/%m/%y", encoding_format: str = "utf8", cls: str = "Core", verbose: bool = True, debug: bool = True, formated: bool = True):
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
        

    def now(self):
        return datetime.datetime.now().strftime(self.datetime_format)  

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
        formated_message = f"{self.now()} | {self.cls} | {message_type} | {message}"
        return formated_message
    
    def _display(self, message: str, end: str = "\n"):

        print(message, end=end)

    def debug(self, message: str = "[default debug message]"):

        if self._debug is True:
            _message = ""
            if self.formated is True:
                _message = self._format_message('debug', message)
            else:
                _message = message

            self._display(_message)

    def info(self, message: str = "[default info message]"):        

        if self._verbose is True:
            _message = ""
            if self.formated is True:
                _message = self._format_message('info', message)
            else:
                _message = message

            self._display(_message)

    def warning(self, message: str = "[default warning message]"):        

        _message = ""
        if self.formated is True:
            _message = self._format_message('warning', message)
        else:
            _message = message

        self._display(_message)
        
    def error(self, message: str = "[default error message]"):        

        _message = ""
        if self.formated is True:
            _message = self._format_message('error', message)
        else:
            _message = message

        self._display(_message)
    

