from typing import Any, Awaitable, Callable, Dict

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject, User
from fluentogram import TranslatorHub


class TranslatorRunnerMiddleware(BaseMiddleware):
    """
    Middleware for adding a translator runner to the event data based on the user's locale.
    """

    async def __call__(
            self,
            handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
            event: TelegramObject,
            data: Dict[str, Any]
    ) -> Any:
        """
        Middleware handler function.

        Args:
            handler: The next handler to call.
            event: The current Telegram event.
            data: The data dictionary for the current context.

        Returns:
            The result of the next handler.
        """
        user: User = data.get("event_from_user")

        if user:
            hub: TranslatorHub = data.get("_translator_hub")
            data["i18n"] = hub.get_translator_by_locale(locale="ru")  # user.language_code)
            data["language_code"] = "ru"  # user.language_code

        return await handler(event, data)
