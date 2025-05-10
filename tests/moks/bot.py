from typing import TYPE_CHECKING, Any, Optional

from aiogram import Bot
from aiogram.methods import TelegramMethod
from aiogram.methods.base import Response, TelegramType
from aiogram.types import ResponseParameters, User

from tests.moks.session import SessionMock


class BotMock(Bot):
    if TYPE_CHECKING:
        session: SessionMock

    def __init__(self, **kwargs :Any) -> None:
        super().__init__(
            kwargs.pop("token", "42:TEST"),
            session=SessionMock(),
            **kwargs,
        )
        self._me = User(
            id=self.id,
            is_bot=True,
            first_name="BotName",
            last_name="BotSurname",
            username="bot",
            language="en-US",
        )

    def add_result_for(
            self,
            method: type[TelegramMethod[TelegramType]],
            ok: bool,
            result: TelegramType | None = None,
            description: Optional[str] = None,
            error_code: int = 200,
            migrate_to_chat_id: Optional[int] = None,
            retry_after: Optional[int] = None,
    ) -> Response[TelegramType]:
        response = Response[method.__returning__](  # type: ignore
            ok=ok,
            result=result,
            description=description,
            error_code=error_code,
            parameters=ResponseParameters(
                migrate_to_chat_id=migrate_to_chat_id,
                retry_after=retry_after,
            ),
        )
        self.session.add_result(response)

        return response

    def get_request(self) -> TelegramMethod[TelegramType]:
        return self.session.get_request()
