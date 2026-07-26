"""
==================================================
SCOOBA

Intent Definitions

Author: Sachin
==================================================
"""

from enum import Enum


class Intent(Enum):

    GREETING = "greeting"

    HOW_ARE_YOU = "how_are_you"

    CREATOR = "creator"

    THANKS = "thanks"

    EXIT = "exit"

    UNKNOWN = "unknown"