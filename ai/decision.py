"""
==================================================
SCOOBA

Decision Object

Author: Sachin
==================================================
"""

from dataclasses import dataclass
from typing import Optional


@dataclass
class Decision:

    # Main intent
    intent: Optional[str] = None

    # Main entity
    # Examples:
    # youtube
    # github
    # hello.py
    entity: Optional[str] = None

    # Optional action
    action: Optional[str] = None

    # Search query
    # Examples:
    # good day
    # python tutorial
    query: Optional[str] = None

    # Target object
    # Examples:
    # hello.py
    # MyProject
    # AI Projects
    target: Optional[str] = None

    # Optional location/path
    location: Optional[str] = None

    # AI confidence
    confidence: float = 0.0

    # Assistant response
    response: Optional[str] = None