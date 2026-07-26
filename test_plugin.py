from plugins.manager import PluginManager

manager = PluginManager()

manager.register(
    "hello",
    lambda: print("Hello Plugin")
)

manager.register(
    "bye",
    lambda: print("Bye Plugin")
)

print(manager.list_plugins())

manager.execute("hello")

manager.execute("bye")