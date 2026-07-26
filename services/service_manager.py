"""
==================================================
SCOOBA

Service Manager

Purpose:
Starts and stops services based on configuration.

Author: Sachin
Version: 0.6.0
==================================================
"""

from utils.logger import logger


class ServiceManager:

    def __init__(self, config):
        self.config = config
        self.services = {}

    def register(self, name, service):
        self.services[name] = service

    def start_all(self):

        logger.info("Starting registered services...")

        enabled_services = self.config.get("services", {})

        for name, service in self.services.items():

            config_key = name.lower().replace(" service", "")

            if enabled_services.get(config_key, False):

                logger.info(f"Starting {name}...")

                service.start()

            else:

                logger.info(f"{name} is disabled.")

    def stop_all(self):

        logger.info("Stopping services...")

        for service in self.services.values():
            service.stop()

    def status(self):

        return {
            name: service.status()
            for name, service in self.services.items()
        }