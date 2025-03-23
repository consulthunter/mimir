import os
import logging
from datetime import datetime
from warnings import catch_warnings


class Logger:
    def __init__(self, log_dir, day, command=None, id=None):
        self.log_dir = log_dir
        self.day = day
        self.command = command
        self.id = id
        self.logger: logging.Logger = self._setup_logger()
        self.log_file = ""

    def _setup_logger(self):
        runtime = datetime.now()
        current_time = runtime.strftime("%H-%M-%S")

        if self.id and self.command and self.day:
            self.log_file = os.path.join(self.log_dir, self.day, self.command, self.id, f"{self.id}_{current_time}.log")
        elif self.command and self.day:
            self.log_file = os.path.join(self.log_dir, self.day, self.command, f"{current_time}.log")

        self._ensure_directory_exists()

        logger = logging.getLogger(self.log_file)
        if not logger.hasHandlers():
            try:
                handler = logging.FileHandler(self.log_file)
                formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
                handler.setFormatter(formatter)
                logger.addHandler(handler)
                logger.setLevel(logging.DEBUG)
            except OSError:
                print("Failed to create log file")
        return logger

    def _ensure_directory_exists(self):
        directory = os.path.dirname(self.log_file)
        if not os.path.exists(directory):
            os.makedirs(directory)

    def log_info(self, message):
        self.logger.info(message)

    def log_error(self, message):
        self.logger.error(message)

    def log_debug(self, message):
        self.logger.debug(message)
