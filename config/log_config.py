import os
import sys
import logging
import logging.config
import traceback
from functools import wraps
from inspect import iscoroutinefunction
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Callable

from icecream import install

from config import app_settings

# Install IceCream for debugging
install()

# Configure the logger
logger = logging.getLogger()

# Set log level from config
LOGS_LEVEL = getattr(logging, app_settings.logs.level)
logger.setLevel(LOGS_LEVEL)

logs_dir = os.path.join(Path(__file__).parent.parent, app_settings.logs.dir_name if LOGS_LEVEL > 10 else "tmp")

# Create logs directory if it doesn't exist
os.makedirs(logs_dir, exist_ok=True)

# Define the log filename
filename = os.path.join(logs_dir, app_settings.logs.file_name)

# Define the log format for the file handler
file_formatter = logging.Formatter(app_settings.logs.handlers_format)

# Set up a timed rotating file handler
logs_file_handler = TimedRotatingFileHandler(filename=filename, when=app_settings.logs.time_rotating, interval=1,
                                             encoding="utf-8", backupCount=app_settings.logs.backup_count)
logs_file_handler.suffix = "%Y-%m-%d"
logs_file_handler.setFormatter(file_formatter)

# Set up a stream handler
logs_stream_handler = logging.StreamHandler(stream=sys.stdout)
logs_stream_handler.setFormatter(file_formatter)

# Add the file handler to the logger
logger.addHandler(logs_file_handler)
logger.addHandler(logs_stream_handler)


def exception_handler(exc_type, exc_value, exc_traceback) -> None:
    """
    Logs uncaught exceptions with full traceback information.
    This handler ignores KeyboardInterrupt to allow clean shutdowns.

    Args:
        exc_type: The type of the exception.
        exc_value: The exception instance.
        exc_traceback: The traceback object.
    """
    if exc_type.__name__ == "KeyboardInterrupt":
        return

    # Format the traceback into a string
    tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # Log the formatted traceback
    logging.error("\n%s", tb_str)


# Set the custom exception handler
sys.excepthook = exception_handler


def log_return_value(method: Callable) -> Callable:
    """
    Decorator to log the return value of a function.

    Supports both synchronous and asynchronous functions.
    Logs the function name and its returned result after execution.

    Args:
        method (Callable): The function to be decorated.

    Returns:
        Callable: The wrapped function that logs its return value.
    """
    log_message = "Function {method_name} returned: {result}"

    @wraps(method)
    async def async_wrapper(*args, **kwargs) -> Callable:
        result = await method(*args, **kwargs)
        logger.info(log_message.format(method_name=method.__name__, result=result))

        return result

    @wraps(method)
    def wrapper(*args, **kwargs) -> Callable:
        result = method(*args, **kwargs)
        logger.info(log_message.format(method_name=method.__name__, result=result))

        return result

    if iscoroutinefunction(method):
        return async_wrapper

    return wrapper
