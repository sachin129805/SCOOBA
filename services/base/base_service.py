"""
==================================================
SCOOBA

Base Service

Purpose:
Defines the standard interface that every SCOOBA
service must follow.

Author: Sachin
Version: 0.4.0
==================================================
"""

from abc import ABC, abstractmethod


class BaseService(ABC):
    """
    Abstract base class for all SCOOBA services.
    """

    @abstractmethod
    def start(self):
        """Start the service."""
        pass

    @abstractmethod
    def stop(self):
        """Stop the service."""
        pass

    @abstractmethod
    def status(self):
        """Return the service status."""
        pass