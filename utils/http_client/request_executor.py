from collections.abc import Awaitable
from functools import wraps
from typing import Any, Callable, TypeVar

import aiohttp
from aiohttp import ClientResponse

from config.log_config import logger

R = TypeVar("R")


def request_executor(method: str = "GET") -> Callable[
    [Callable[[ClientResponse, dict[str, Any]],
    Awaitable[R]]],
    Callable[..., Awaitable[R]]
]:
    """
    Wrap an HTTP request function with aiohttp session and error handling.

    Args:
        method (str): HTTP method to use (default: "GET").

    Returns:
        Callable: Decorator that injects a ClientResponse into the wrapped function.
    """
    def decorator(func: Callable[[ClientResponse, Any], Awaitable[R]]) -> Callable[..., Awaitable[R]]:
        @wraps(func)
        async def wrapper(*args: Any, **kwargs: Any) -> Any:
            url: str = kwargs.pop("url", "")

            if not url:
                raise ValueError("Missing required 'url' parameter")

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.request(method=method.upper(), url=url, **kwargs) as response:
                        return await func(response, *args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    raise

        return wrapper

    return decorator
