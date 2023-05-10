import configparser


class Config:
    def __init__(self, config_file):
        self.config_file = config_file
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def get_sections(self):
        return self.config.sections()

    def get_options(self, section):
        return self.config.options(section)

    def get(self, section, option):
        return self.config.get(section, option)
