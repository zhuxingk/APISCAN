import logging

class LogManager:
    def __init__(self, logger_name):
        self.logger_name = logger_name

    def get_logger(self):
        logger = logging.getLogger(self.logger_name)
        return logger

    def add_console_handler(self, logger):
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter('%(levelname)s - %(message)s')
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

    def add_file_handler(self, logger, filename):
        file_handler = logging.FileHandler(filename)
        formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    def get_logger_and_add_handlers(self, filename=None):
        logger = self.get_logger()
        self.add_console_handler(logger)
        if filename:
            self.add_file_handler(logger, filename)
        return logger

    def log_info(self, message):
        logger = self.get_logger()
        logger.info(message)

    def log_debug(self, message):
        logger = self.get_logger()
        logger.debug(message)

    def log_warning(self, message):
        logger = self.get_logger()
        logger.warning(message)

    def log_error(self, message):
        logger = self.get_logger()
        logger.error(message)

    def debug(self, param):
        pass
