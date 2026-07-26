"""
==================================================
SCOOBA

Plugin Manager

Author: Sachin
==================================================
"""


class PluginManager:

    def __init__(self):

        self.plugins = {}

    def register(self, name, plugin):

        self.plugins[name] = plugin

    def get(self, name):

        return self.plugins.get(name)

    def execute(self, name, *args, **kwargs):

        plugin = self.get(name)

        if plugin is None:

            return None

        return plugin(*args, **kwargs)

    def list_plugins(self):

        return list(self.plugins.keys())