"""
==================================================
SCOOBA

Logger Service

Author: Sachin
Version: 0.4.0
==================================================
"""

from services.base.base_service import BaseService
from utils.logger import logger


class LoggerService(BaseService):

    def __init__(self):
        self.running = False

    def start(self):
        self.running = True
        logger.info("Logger Service Started")

    def stop(self):
        self.running = False
        logger.info("Logger Service Stopped")

    def status(self):
        return "Running" if self.running else "Stopped"