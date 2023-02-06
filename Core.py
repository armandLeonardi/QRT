"""
This script containt classes:
    - Core: a class offering basic functionalites such as formated display, configuration loading, log file management
    - Base64Engine: a class offering the possibilities to encode/decode string in base64

You can check on the '__main__' part to see how to use thoose classes
Ael - 02FEB23
"""
import datetime
import json
import os
import base64

class Core:
    """
    Class with allow to:
    - manage standard output message (depending of verbose level)
    - allow to load a json configuration
    - open a log file
    """

    def __init__(self, path_config: str = "" ,datetime_format: str = "%d/%m/%y %H:%M:%S", encoding_format: str = "utf8", cls: str = "Core", verbose: bool = True, debug: bool = True, formated: bool = True, *args, **kargs) -> None:
        """Core class constructor

        Args:
            path_config (str, optional): path to your configuration json file. Defaults to "".
            datetime_format (_type_, optional): display format for datetime. Defaults to "%d/%m/%y %H:%M:%S".
            encoding_format (str, optional): encoding format for/from files. Defaults to "utf8".
            cls (str, optional): class name. Usefull for displaying debug. Defaults to "Core".
            verbose (bool, optional): true if you want to display message on standard output. False otherwise. Defaults to True.
            debug (bool, optional): true if you want to display message on standard output on deeper level. False otherwise. Defaults to True.
            formated (bool, optional): true if you want to add informations on you displayed messages. Raw message otherwise. Defaults to True.
        """
        self.__version__ = "1.0.0"
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

    def now(self, datetime_format: str = "") -> str:
        """Return the current system date depending of datetime_format.
        Input format replace the congiruation format.

        Args:
            datetime_format (str, optional): on the fly datetime format. Defaults to "".

        Returns:
            str: system time with given format.
        """
        datetime_format = datetime_format if datetime_format != "" else self.datetime_format
        return datetime.datetime.now().strftime(datetime_format)  

    def load_config(self) -> None:
        """Load the configuration json file set on the attribute: path_config

        Raises:
            ValueError: if path_config is empty
        """

        config = {}

        # if path_config attribute is empty
        if self.path_config == "":
            raise ValueError("Confguration path is empty")
        else:
            with open(self.path_config, 'r', encoding=self.encoding_format) as f:
                config = json.load(f)
                f.close()

                # set values on current loaded object.
                # Keys present on the configuration but not in the object was never loaded
                for key, value in config.items():
                    if key in self.__dict__:
                        self.__setattr__(key, value)

    def _format_message(self, message_type: str, message: str) -> str:
        """Format the message in input.

        Format: system_time | current_class | message_type | message

        Args:
            message_type (str): type of message. Could be idealy (debug, info, warning, error) 
            message (str): message to message.

        Returns:
            str: formated message.
        """

        formated_message = f"{self.now()} | {self.cls: <9} | {message_type: <9} | {message}"
        return formated_message
    
    def _display(self, message: str, end: str = "\n") -> None:
        """Display the message in input on standard output.
            Defaulty add a chariot return at the end.

        Args:
            message (str): message to display
            end (str, optional): end line charater to add. Defaults to "\n".
        """

        print(message, end=end)

    def open_log_file(self) -> None:
        """Open the log file set on path_log_folder attribute.

        By default create a log file as follow:
                [system_time]_[current_class].log
        By example:
                06022023130332_myObject.log

        This format allow to quicly identify your log with created object and time creating.
        Very usefull with Linux grep/ls commands.
            
        """

        # only if the log folder was precise
        if self.path_log_folder != "":
            _now = self.now(datetime_format="%d%m%y%H%M%S")
            log_filename = f"{_now}_{self.cls}.log"

            # create the full path of current log file.
            full_path_log_filename = os.path.join(self.path_log_folder, log_filename)
            self.filename_log = full_path_log_filename

            # open a text file
            self.logger = open(full_path_log_filename, 'a', encoding=self.encoding_format)
            self.logger_open = True

        else:

            # inform user, the log folder path is empty.
            # this is considered as cirtical error.
            self.warning("Log folder path is empty")

    def set_logger(self, other) -> None:
        """Allow to connect a logger (stream file) from an object to another.
        Typicaly, if you want a child object write logs on the same file as parent object.
        
        IMPORTANT REMARK: Both must be heritate from Core class.

        Example:

        class A:

            def foo(self):
                self.info("something...")

        class B:

            def bar(self):

                self.open_log_file()
                a = A()
                a.set_logger(self)


        Args:
            other (any): an ohter object. Must heritate from Core class too. 
        """

        if 'logger' in other.__dict__:
            if other.logger is not None:
                self.logger = other.logger
                self.logger_open = True

    def write_log(self, message: str, end: str = "\n") -> None:
        """Write the message in input on the file open by logger attribute.

        Args:
            message (str): message you want to log.
            end (str, optional): end line charater to add. Defaults to "\n".
        """

        if self.logger_open is True:
            try:
                self.logger.write(f"{message}{end}")
                self.logger.flush() # allow to write and save as same time. Target file is imedialty update.
            except Exception as error:
                self.error(error)

    def close_log(self) -> None:
        """Close the current openend file.
        """

        try:
            self.logger.close()
            self.logger_open = False
            self.info(f"Closing log folder {self.filename_log}")
        except Exception as error:
            self.error(error)

    def debug(self, message: str = "[default debug message]") -> None:
        """Display and write on log a debug message.
        Work only if 'bebug' attribute is True. Do nothing otherwise.

        Remark: log writing is done only if a log folder is open. Do nothing otherwise.

        Args:
            message (str, optional): message to display or log. Defaults to "[default debug message]".
        """

        _message = ""
        if self.formated is True: # format it if require
            _message = self._format_message('debug', message)
        else:
            _message = message

        if self._debug is True:
            self._display(_message) # standart output displaying

        self.write_log(_message) # log writing

    def info(self, message: str = "[default info message]"):        
        """Display and write on log a information message (basic informations).
        Work only if 'verbose' attribute is True. Do nothing otherwise.

        Remark: log writing is done only if a log folder is open. Do nothing otherwise.

        Args:
            message (str, optional): message to display or log. Defaults to "[default info message]".
        """

        _message = ""
        if self.formated is True:
            _message = self._format_message('info', message)
        else:
            _message = message

        if self._verbose is True:
            self._display(_message)

        self.write_log(_message)

    def warning(self, message: str = "[default warning message]"):        
        """Display and write on log a warning message (for cases considerd as a potential issue but not critical).
        No verbose or debug restriction.

        Remark: log writing is done only if a log folder is open. Do nothing otherwise.

        Args:
            message (str, optional): message to display or log. Defaults to "[default warning message]".
        """

        _message = ""
        if self.formated is True:
            _message = self._format_message('warning', message)
        else:
            _message = message

        self.write_log(_message)
        self._display(_message)
        
    def error(self, message: str = "[default error message]"):        
        """Display and write on log a error message (for cases considerd as critical error and script should be stop).
        No verbose or debug restriction.

        Remark: log writing is done only if a log folder is open. Do nothing otherwise.

        Args:
            message (str, optional): message to display or log. Defaults to "[default error message]".
        """

        _message = ""
        if self.formated is True:
            _message = self._format_message('error', message)
        else:
            _message = message

        self.write_log(_message)
        self._display(_message)


class Base64Engine:
    """A tiny class used as base64 encoder of decoder.
    """
    encoding = "utf8" # default encoding.

    @classmethod
    def encode(cls, chars: str) -> str:
        """Return the base64 result of the input string.

        Args:
            chars (str): string to convert on base64.

        Returns:
            str: converted string.
        """
        chars = str(chars)
        return base64.b64encode(chars.encode(encoding=Base64Engine.encoding)).decode(encoding=Base64Engine.encoding)
    
    @classmethod
    def decode(cls, chars64: str) -> str:
        """Return the normal string of the base64 inputs string.
        Error occur, if your input string wasn't on base64.

        Args:
            chars64 (str): base645 input string

        Returns:
            str: normal converted input string.
        """
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
