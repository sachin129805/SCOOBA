"""
==================================================
SCOOBA

Base Skill SDK

Author: Sachin
==================================================
"""

from abc import ABC, abstractmethod


class Skill(ABC):

    @property
    @abstractmethod
    def name(self):
        pass

    @abstractmethod
    def can_handle(self, decision):
        pass

    @abstractmethod
    def execute(self, decision):
        pass