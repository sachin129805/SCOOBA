"""
==================================================
SCOOBA

Base Text-To-Speech Provider

Author: Sachin
==================================================
"""

from abc import ABC, abstractmethod


class BaseTTSProvider(ABC):

    @abstractmethod
    def speak(self, text: str):
        """Speak the supplied text."""
        pass