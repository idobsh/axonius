import logging
import pytest
from helpers.logger_helper import get_logger

@pytest.fixture(scope="session", autouse=True)
def logger_fixture():
    logger = get_logger("test_session")
    
    # Ensure global logging is configured
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.INFO)

    # Prevent duplicate logs if already configured
    if not root_logger.handlers:
        console_handler = logging.StreamHandler()
        formatter = logging.Formatter(
            "%(asctime)s [%(levelname)8s] %(message)s (%(filename)s:%(lineno)s)"
        )
        console_handler.setFormatter(formatter)
        root_logger.addHandler(console_handler)

    return logger

@pytest.fixture(autouse=True)
def inject_logger(request, logger_fixture):
    # Automatically attach logger to any test class or function
    if hasattr(request.node, "cls") and request.node.cls:
        setattr(request.node.cls, "logger", logger_fixture)
    elif hasattr(request, "function"):
        request.function.logger = logger_fixture