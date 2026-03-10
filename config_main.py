from config_reader import ConfigReader
from config_editor import ConfigEditor

CONFIG_FILE = "config.ini"

# Read values
reader = ConfigReader(CONFIG_FILE)
print("Database host:", reader.get_value("database", "host"))

# Edit values
editor = ConfigEditor(CONFIG_FILE)
editor.set_value("database", "host", "127.0.0.1")
editor.set_value("app", "debug", "false")
editor.save()

print("Config updated.")
