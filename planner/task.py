"""
==================================================
SCOOBA

Task

Author: Sachin
==================================================
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Task:

    # Skill responsible for execution
    #
    # Examples:
    # browser
    # filesystem
    # developer

    skill: str

    # Action to perform
    #
    # Examples:
    # open
    # search
    # play_first
    # create_file

    action: str

    # Main entity
    #
    # Examples:
    # youtube
    # google
    # hello.py

    entity: Optional[str] = None

    # Optional search/query data
    #
    # Examples:
    # Avicii
    # SB737
    # Python tutorials

    query: Optional[str] = None

    # Optional target

    target: Optional[str] = None