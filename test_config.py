from config.manager import ConfigManager

config = ConfigManager()

print(config.get("workspace"))

print(config.get("voice", "model"))

print(config.get("developer", "default_ide"))

print(config.get("developer", "create_git"))

print(config.get("developer", "create_venv"))