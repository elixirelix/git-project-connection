from logging import getLogger, DEBUG, Formatter, FileHandler, StreamHandler, Filter
from datetime import datetime
from os import getenv

class Filtering(Filter):
    def filter(self, record):
        return record.name == "root"

logger = getLogger(getenv("LOGGER_NAME"))
logger.setLevel(DEBUG)

formatter = Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s] [%(message)s]"
)

file_handler = FileHandler(
    f'logs/{str(datetime.now()).split(" ")[0]}.log'
)
file_handler.setLevel(DEBUG)
file_handler.setFormatter(formatter)

console_handler = StreamHandler()
console_handler.setLevel(DEBUG)
console_handler.setFormatter(formatter)
console_handler.addFilter(Filtering())

logger.addHandler(file_handler)
logger.addHandler(console_handler)