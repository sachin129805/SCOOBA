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

    intent: Optional[str] = None

    entity: Optional[str] = None

    action: Optional[str] = None

    confidence: float = 0.0

    response: Optional[str] = None