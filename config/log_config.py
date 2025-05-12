import logging
import logging.config
import os
import sys
import traceback
from functools import wraps
from inspect import iscoroutinefunction
from logging.handlers import TimedRotatingFileHandler
from pathlib import Path
from typing import Any

from icecream import install

from config import app_settings

# Install Icecream for easier debugging output
install()

# Initialize root logger
logger = logging.getLogger()

# Set logging level based on config
logs_level = getattr(logging, app_settings.logs.level)
logger.setLevel(logs_level)

# Use "tmp" directory for logs if level is DEBUG or lower (<=10)
logs_dir = os.path.join(Path(__file__).parent.parent, app_settings.logs.dir_name if logs_level > 10 else "tmp")

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


def exception_handler(exc_type: Any, exc_value: Any, exc_traceback: Any) -> None:
    """
    Custom exception handler that logs uncaught exceptions with traceback.

    Skips KeyboardInterrupt to allow graceful shutdown.

    Args:
        exc_type (Any): Exception class/type.
        exc_value (Any): Exception instance.
        exc_traceback (Any): Traceback object.
    """
    if exc_type.__name__ == "KeyboardInterrupt":
        return

    # Format the traceback into a string
    tb_str = "".join(traceback.format_exception(exc_type, exc_value, exc_traceback))

    # Log the formatted traceback
    logging.error("\n%s", tb_str)


# Set the custom exception handler
sys.excepthook = exception_handler


def log_return_value(method: Any) -> Any:
    """
    Decorator that logs the return value of a function (sync or async).

    Args:
        method (Callable): Target function to wrap.

    Returns:
        Callable: Wrapped function with logging.
    """
    log_message = "Function {method_name} returned: {result}"

    @wraps(method)
    async def async_wrapper(*args: Any, **kwargs: dict[Any, Any]) -> Any:
        result = await method(*args, **kwargs)
        logger.info(log_message.format(method_name=method.__name__, result=result))

        return result

    @wraps(method)
    def wrapper(*args: Any, **kwargs: dict[Any, Any]) -> Any:
        result = method(*args, **kwargs)
        logger.info(log_message.format(method_name=method.__name__, result=result))

        return result

    if iscoroutinefunction(method):
        return async_wrapper

    return wrapper
