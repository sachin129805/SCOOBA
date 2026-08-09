"""
==================================================
SCOOBA

AI Decision

Author: Sachin
==================================================
"""

from dataclasses import dataclass, field
from typing import Optional, List


@dataclass
class Decision:

    # ==================================================
    # CORE
    # ==================================================

    intent: Optional[str] = None

    entity: Optional[str] = None

    action: Optional[str] = None

    # ==================================================
    # QUERY
    # ==================================================

    query: Optional[str] = None

    # ==================================================
    # TARGET
    # ==================================================

    target: Optional[str] = None

    # ==================================================
    # LOCATION
    # ==================================================

    location: Optional[str] = None

    # ==================================================
    # VIDEO POSITION
    # ==================================================

    position: Optional[int] = None

    # ==================================================
    # ORIGINAL COMMAND
    # ==================================================

    command: Optional[str] = None

    # ==================================================
    # CONFIDENCE
    # ==================================================

    confidence: float = 0.0

    # ==================================================
    # RESPONSE
    # ==================================================

    response: Optional[str] = None

    # ==================================================
    # MULTI-STEP DECISIONS
    # ==================================================
    #
    # Example:
    #
    # "open youtube and search avicii and play
    #  the third video"
    #
    # becomes:
    #
    # steps = [
    #     OPEN_APP,
    #     SEARCH,
    #     PLAY_VIDEO
    # ]
    #
    # ==================================================

    steps: List["Decision"] = field(
        default_factory=list
    )