"""
==================================================
SCOOBA

Task

Author: Sachin
==================================================
"""

from dataclasses import dataclass


@dataclass
class Task:

    skill: str
    action: str
    entity: str = None