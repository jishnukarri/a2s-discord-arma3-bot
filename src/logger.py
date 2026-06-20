import logging
from src.config import LOGGING_FILE

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG) 

    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s : %(message)s"
    )
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    handler = logging.FileHandler(filename=LOGGING_FILE)
    handler.setLevel(logging.INFO)
    handler.setFormatter(formatter)
    logger.addHandler(handler)
