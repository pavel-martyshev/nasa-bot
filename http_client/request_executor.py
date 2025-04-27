from functools import wraps

import aiohttp
from icecream import ic


def async_request_executor(method: str = "GET"):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            session_request_data = {"method": method.upper(), **kwargs}

            async with aiohttp.ClientSession() as session:
                async with session.request(**session_request_data) as response:
                    try:
                        return await func(response=response, *args, **kwargs)
                    except Exception as e:
                        ic(e)
                    finally:
                        await session.close()

        return wrapper

    return decorator
