import configparser

class ConfigReader:
    def __init__(self, file_path):
        self.file_path = file_path
        self.config = configparser.ConfigParser()
        self.config.read(file_path)

    def get_value(self, section, key):
        if self.config.has_section(section) and self.config.has_option(section, key):
            return self.config.get(section, key)
        return None

    def get_section(self, section):
        if self.config.has_section(section):
            return dict(self.config.items(section))
        return {}
