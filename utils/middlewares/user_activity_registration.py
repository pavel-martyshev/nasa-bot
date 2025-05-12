import time
from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from tortoise.contrib.pydantic import PydanticModel

from database.postgres.core.CRUD.user import UserCrud

user_crud = UserCrud()


class UserActivityRegistrationMiddleware(BaseMiddleware):
    """
    Middleware that registers or updates user activity on each incoming event.

    Creates the user if not present, and updates last_activity_time.
    """
    async def __call__(
            self,
            handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: dict[str, Any]
    ) -> Any:
        """
        Track and update user activity before handling the event.

        Args:
            handler (Callable): Next handler in the middleware chain.
            event (TelegramObject): Incoming Telegram event.
            data (dict[str, Any]): Contextual data for the event.

        Returns:
            Any: Result from the next handler.
        """
        event_from_user: User = data["event_from_user"]

        if event_from_user:
            crud_kwargs = {
                "telegram_id": event_from_user.id,
                "username": event_from_user.username,
                "first_name": event_from_user.first_name,
                "last_name": event_from_user.last_name,
                "language_code": event_from_user.language_code,
                "last_activity_time": int(time.time()),
            }

            user: PydanticModel | None = await user_crud.get_or_create(**crud_kwargs)
            await user_crud.update(filters={"id": user.id}, last_activity_time=int(time.time()))  # type: ignore[union-attr]

        return await handler(event, data)
