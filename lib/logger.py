from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler, Filter
from datetime import datetime
from os import getenv


class Filtering(Filter):
    def filter(self, record):
        return record.name == "root"

class CustomFormatter(Formatter):
    def __init__(self, is_console=False):
        super().__init__()
        self.is_console = is_console

    def format(self, record):
        if hasattr(record, "file"):
            self._style._fmt = (
                "[%(asctime)s] [%(levelname)s] "
                "[%(name)s] [%(file)s] [%(message)s]"
            )
        else:
            self._style._fmt = (
                "[%(asctime)s] [%(levelname)s] "
                "[%(name)s] [%(message)s]"
            )

        return super().format(record)

logger = getLogger(getenv("LOGGER_NAME"))
logger.setLevel(DEBUG)

file_formatter = CustomFormatter(is_console=False)
console_formatter = CustomFormatter(is_console=True)

file_handler = FileHandler(
    f'logs/{str(datetime.now()).split(" ")[0]}.log'
)
file_handler.setLevel(DEBUG)
file_handler.setFormatter(file_formatter)

console_handler = StreamHandler()
console_handler.setLevel(DEBUG)
console_handler.setFormatter(console_formatter)
console_handler.addFilter(Filtering())

logger.addHandler(file_handler)
logger.addHandler(console_handler)