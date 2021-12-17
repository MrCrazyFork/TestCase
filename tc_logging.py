import logging
import config
from logging.handlers import RotatingFileHandler

logger = logging.getLogger("TestCase")
hdlr = RotatingFileHandler(config.LOG_NAME, mode='a', maxBytes=10 * 1024 * 1024, backupCount=1, encoding="utf-8", delay=False)
formatter = logging.Formatter("%(asctime)s;%(levelname)s;%(message)s")
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(20)
