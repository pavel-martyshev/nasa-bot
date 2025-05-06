import time
from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from tortoise.contrib.pydantic import PydanticModel

from database.postgres.core.CRUD.user import UserCRUD

user_crud = UserCRUD()


class UserActivityRegistrationMiddleware(BaseMiddleware):
    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
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

            user: PydanticModel = await user_crud.get_or_create(**crud_kwargs)
            await user_crud.update(filters={"id": user.id}, last_activity_time=int(time.time()))

        return await handler(event, data)
