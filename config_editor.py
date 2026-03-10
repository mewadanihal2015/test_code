import configparser

class ConfigEditor:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    def set_value(self, section, key, value):
        if not self.config.has_section(section):
            self.config.add_section(section)
        self.config.set(section, key, str(value))

    def remove_key(self, section, key):
        if self.config.has_section(section):
            self.config.remove_option(section, key)

    def remove_section(self, section):
        self.config.remove_section(section)

    def save(self):
        with open(self.file_path, "w") as configfile:
            self.config.write(configfile)
