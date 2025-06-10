from collections.abc import Awaitable
from typing import Any, Callable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    """
    Middleware that injects a TranslatorRunner into event data based on user's locale.
    """

    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any],
    ) -> Any:
        """
        Add translator and language code to context data for localization support.

        Args:
            handler (Callable): Next handler in the middleware chain.
            event (TelegramObject): Incoming Telegram event.
            data (dict[str, Any]): Contextual data for the event.

        Returns:
            Any: Result from the next handler.
        """
        user: User | None = data.get("event_from_user")

        if user:
            hub: TranslatorHub = data.get("_translator_hub")
            data["i18n"] = hub.get_translator_by_locale(locale=user.language_code)
            data["language_code"] = user.language_code

        return await handler(event, data)
