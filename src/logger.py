import logging
from src.config import LOGGING_FILE

def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler(filename=LOGGING_FILE)
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s : %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
