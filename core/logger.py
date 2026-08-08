"""
=========================================================
SCOOBA

Professional Logger
=========================================================
"""

import logging
from pathlib import Path

from config.manager import ConfigManager


class Logger:

    _instance = None

    def __new__(cls):

        if cls._instance is None:
            cls._instance = super().__new__(cls)

        return cls._instance

    def __init__(self):

        if hasattr(self, "_initialized"):
            return

        config = ConfigManager()

        log_level = config.get("logging", "level").upper()
        log_file = config.get("logging", "file")

        Path(log_file).parent.mkdir(
            parents=True,
            exist_ok=True
        )

        self.logger = logging.getLogger("SCOOBA")

        self.logger.setLevel(
            getattr(logging, log_level, logging.INFO)
        )

        formatter = logging.Formatter(
            "[%(asctime)s] [%(levelname)s] %(message)s",
            "%Y-%m-%d %H:%M:%S"
        )

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)

        file_handler = logging.FileHandler(
            log_file,
            encoding="utf-8"
        )
        file_handler.setFormatter(formatter)

        if not self.logger.handlers:
            self.logger.addHandler(console_handler)
            self.logger.addHandler(file_handler)

        self._initialized = True

    def info(self, message):
        self.logger.info(message)

    def warning(self, message):
        self.logger.warning(message)

    def error(self, message):
        self.logger.error(message)

    def debug(self, message):
        self.logger.debug(message)

    def critical(self, message):
        self.logger.critical(message)


logger = Logger()