from functools import wraps

import aiohttp

from config.log_config import logger


def request_executor(method: str = "GET"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            request_data = {"method": method.upper(), **kwargs}

            async with aiohttp.ClientSession() as session:
                try:
                    async with session.request(**request_data) as response:
                        return await func(response, *args, **kwargs)
                except Exception as e:
                    logger.error(e)
                    raise

        return wrapper
    return decorator
