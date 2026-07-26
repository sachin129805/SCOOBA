"""
==================================================
SCOOBA

Application State

Purpose:
Tracks the current operating state of SCOOBA.

Author: Sachin
==================================================
"""

from enum import Enum


class AssistantState(Enum):

    BOOTING = "BOOTING"

    READY = "READY"

    LISTENING = "LISTENING"

    THINKING = "THINKING"

    SPEAKING = "SPEAKING"

    SHUTDOWN = "SHUTDOWN"