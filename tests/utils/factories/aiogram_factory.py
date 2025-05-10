from random import randint
from typing import Optional

from aiogram.enums import ChatType
from aiogram.types import Chat, User


class AiogramFactory:
    @staticmethod
    def get_chat_instance(chat_type: str = ChatType.PRIVATE) -> Chat:
        return Chat(id=randint(1000000, 9999999), type=chat_type)

    @staticmethod
    def get_user_instance(
            *,
            user_id: Optional[int] = None,
            first_name: str = "User",
            language_code: str = "en") -> User:
        return User(
            id=user_id if user_id else randint(1000000, 9999999),
            is_bot=False,
            first_name=first_name,
            language_code=language_code
        )
