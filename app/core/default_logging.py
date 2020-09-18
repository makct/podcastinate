import logging

from core.settings import LOG_PATH


def _get_file_logger() -> logging.Logger:
    fmt = f"[%(asctime)s] - %(message)s"

    logger = logging.getLogger("file_logger")
    logger.setLevel(logging.INFO)
    ch = logging.FileHandler(LOG_PATH)
    ch.setFormatter(logging.Formatter(fmt))
    logger.addHandler(ch)

    return logger


file_logger = _get_file_logger()
