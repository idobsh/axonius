import logging
import sys

def get_logger(name: str = "test_logger") -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    if not logger.handlers:
        # Console handler
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.DEBUG)

        # Format
        formatter = logging.Formatter(
            "[%(asctime)s] %(levelname)s - %(name)s - %(message)s", "%H:%M:%S"
        )
        console_handler.setFormatter(formatter)

        logger.addHandler(console_handler)

    return logger
