import pytest
from helpers.logger_helper import get_logger

@pytest.fixture(scope="session", autouse=True)
def logger_fixture():
    logger = get_logger("test_session")
    return logger

@pytest.fixture(autouse=True)
def inject_logger(request, logger_fixture):
    # Automatically attach logger to any test class or function
    if hasattr(request.node, "cls") and request.node.cls:
        setattr(request.node.cls, "logger", logger_fixture)
    elif hasattr(request, "function"):
        request.function.logger = logger_fixture