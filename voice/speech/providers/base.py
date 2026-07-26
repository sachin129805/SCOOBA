"""
==================================================
SCOOBA

Base Speech Provider

Purpose:
Defines the interface for all speech recognition
providers.

Author: Sachin
==================================================
"""

from abc import ABC, abstractmethod


class BaseSpeechProvider(ABC):
    """
    Base interface for speech recognition engines.
    """

    @abstractmethod
    def listen(self) -> str:
        """
        Listen and return recognised text.
        """
        pass