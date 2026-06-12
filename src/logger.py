import logging


def setup_logging():
    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    handler = logging.FileHandler("a2s-main.log")
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s : %(message)s"
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)
