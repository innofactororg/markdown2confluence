import os
from logging.handlers import RotatingFileHandler
import logging


class Logger:
    def __init__(
        self,
        name: str,
        log_file: str = 'markdown2confluence.log',
        level: int = logging.DEBUG if os.getenv("DEBUG") else logging.INFO
    ):
        """
        Initialize the Logger with a specified name and log file.

        :param name: Name of the logger, usually __name__ is passed
                     to get the module's name.
        :param log_file: File path for the log file.
        :param level: Logging level, default is logging.INFO.
        """
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)

        # Create log directory if it doesn't exist
        log_dir = os.path.dirname(log_file)
        if log_dir and not os.path.exists(log_dir):
            os.makedirs(log_dir)

        # Create a file handler which logs even debug messages
        file_handler = RotatingFileHandler(
            log_file, maxBytes=1024*1024*5, backupCount=5)
        file_handler.setLevel(level)

        console_handler = logging.StreamHandler()
        console_handler.setLevel(level)

        # Create formatter and add it to the handlers
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        console_handler.setFormatter(formatter)

        # Add the handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)

    def get_logger(self):
        """
        Return the configured logger.
        """
        return self.logger
