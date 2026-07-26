"""
==================================================
SCOOBA
Module: Dependency Container

Purpose:
Stores and provides shared services across the
entire application.

Author: Sachin
Version: 0.3.0
==================================================
"""


class ServiceContainer:
    """
    Stores shared service instances.
    """

    def __init__(self):
        self._services = {}

    def register(self, name, instance):
        """
        Register a shared service.
        """
        self._services[name] = instance

    def get(self, name):
        """
        Retrieve a registered service.
        """
        if name not in self._services:
            raise KeyError(f"Service '{name}' is not registered.")

        return self._services[name]

    def exists(self, name):
        """
        Check whether a service exists.
        """
        return name in self._services