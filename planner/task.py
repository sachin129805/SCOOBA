"""
==================================================
SCOOBA

Task Model

Author: Sachin
==================================================
"""

from dataclasses import dataclass, field


@dataclass
class Task:

    action: str

    target: str = ""

    params: dict = field(default_factory=dict)

    status: str = "PENDING"

    def complete(self):

        self.status = "DONE"

    def fail(self):

        self.status = "FAILED"

    def __str__(self):

        return f"{self.action} -> {self.target} [{self.status}]"