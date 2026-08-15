from logging import getLogger, basicConfig, NOTSET
from datetime import datetime

logger = getLogger(__name__)
format = "[%(asctime)s] [%(level)s] [%(file)s] [%(type)s] %(message)s"
basicConfig(filename=f"logs/{str(datetime.now()).split(" ")[0]}.log", level=NOTSET, encoding="UTF-8", filemode="a", format=format)

# logger.info("test", extra={"file": "logger.py", "type": "logger", "level": "INFO"})