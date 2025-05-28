import logging
import sys

def get_logger(name: str) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)

    # Avoid adding multiple handlers if already configured
    if not logger.handlers:
        handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)

    return logger
