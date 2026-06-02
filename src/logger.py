
import logging
import os
from config import LOG_PATH

# create logs folder if it doesn't exist
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def get_logger(name):
    # create logger
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    # avoid duplicate handlers if logger already exists
    if logger.handlers:
        return logger

    # ---- file handler — saves logs to file ----
    file_handler = logging.FileHandler(LOG_PATH)
    file_handler.setLevel(logging.DEBUG)

    # ---- console handler — prints logs to terminal ----
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)

    # ---- format — how each log line looks ----
    formatter = logging.Formatter(
        '%(asctime)s | %(levelname)s | %(name)s | %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )

    file_handler.setFormatter(formatter)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger