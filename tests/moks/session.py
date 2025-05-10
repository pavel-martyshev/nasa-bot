from collections import deque
from collections.abc import AsyncGenerator
from typing import Any, Optional

from aiogram import Bot
from aiogram.client.session.base import BaseSession
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response, TelegramType
from aiogram.types import UNSET_PARSE_MODE


class SessionMock(BaseSession):
    def __init__(self) -> None:
        super().__init__()
        self.responses: deque[Response[Any]] = deque()
        self.requests: deque[TelegramMethod[Any]] = deque()
        self.closed = True

    def add_result(self, response: Response[TelegramType]) -> Response[TelegramType]:
        self.responses.append(response)
        return response

    def get_request(self) -> TelegramMethod[TelegramType]:
        return self.requests.popleft()

    async def close(self) -> None:
        self.closed = True

    async def make_request(
        self,
        bot: Bot,
        method: TelegramMethod[TelegramType],
        timeout: Optional[int] = UNSET_PARSE_MODE
    ) -> TelegramType:
        self.closed = False
        self.requests.append(method)

        response: Response[TelegramType] = self.responses.popleft()
        self.check_response(
            bot=bot,
            method=method,
            status_code=response.error_code or 400,
            content=response.model_dump_json(),
        )

        if not response.result:
            raise ValueError("Response is None")

        return response.result

    async def stream_content(
        self,
        url: str,
        headers: Optional[dict[str, Any]] = None,
        timeout: int = 30,
        chunk_size: int = 65536,
        raise_for_status: bool = True,
    ) -> AsyncGenerator[bytes, None]:
        yield b""
