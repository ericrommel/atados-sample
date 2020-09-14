import datetime
import logging
import sys
from logging.handlers import TimedRotatingFileHandler

is_color_log_presented = True
try:
    import colorlog
except ImportError:
    is_color_log_presented = False


class Log:
    def __init__(self, logfile_name):
        self.log_file_formatter = logging.Formatter("%(asctime)s %(levelname)-8s | %(message)s")
        self.log_file = logfile_name
        self.log_level = logging.DEBUG

    def get_console_handler(self):
        """
        Print out log in the console
        :return: console_handler
        """
        console_handler = logging.StreamHandler(sys.stdout)

        if is_color_log_presented:
            log_stream_format = " %(log_color)s%(asctime)s %(levelname)-8s%(reset)s | %(log_color)s%(message)s%(reset)s"
            # The available color names are 'black', 'red', 'green', 'yellow', 'blue', 'purple', 'cyan' and 'white'.
            log_stream_formatter = colorlog.ColoredFormatter(
                log_stream_format,
                log_colors={
                    "DEBUG": "bold_cyan",
                    "INFO": "white",
                    "WARNING": "bold_yellow",
                    "ERROR": "red",
                    "CRITICAL": "bold_red",
                },
            )
            console_handler.setFormatter(log_stream_formatter)
        else:
            console_handler.setFormatter(self.log_file_formatter)

        return console_handler

    def get_file_handler(self):
        """
        Print out log in the file
        :return: file_handler
        """

        # Use RotatingFileHandler classes, such as the TimedRotatingFileHandler, instead of FileHandler, as it will
        # rotate the file for you automatically when the file reaches a size limit or do it everyday.
        file_handler = TimedRotatingFileHandler(
            filename=datetime.datetime.now().strftime(self.log_file + "_%Y%m%d.log"),
            when="midnight",
        )
        file_handler.setFormatter(self.log_file_formatter)
        return file_handler

    def get_logger(self, logger_name):
        logger = logging.getLogger(logger_name)
        logger.setLevel(self.log_level)
        logger.addHandler(self.get_console_handler())
        logger.addHandler(self.get_file_handler())
        logger.propagate = False
        return logger

        # _log = logging.getLogger("pythonConfig")
        # _log.setLevel(log_level)
        # _log.addHandler(file_handler)
        # _log.addHandler(stream)
        # return _log
