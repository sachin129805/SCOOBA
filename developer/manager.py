"""
==================================================
SCOOBA

Developer Manager

Author: Sachin
==================================================
"""

from developer.python import PythonBuilder


class DeveloperManager:

    def __init__(self):

        self.python = PythonBuilder()

    def create_python_project(self, name):

        return self.python.create(name)