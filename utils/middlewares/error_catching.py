from collections.abc import Awaitable
from typing import Any, Callable, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import DialogManager, StartMode

from config.log_config import logger
from states.states import ErrorDialog


class SafeDialogMiddleware(BaseMiddleware):
    """
    Middleware that catches unhandled exceptions in dialog handlers.

    Logs the exception and redirects the user to a fallback error dialog,
    preventing the bot from appearing unresponsive.
    """
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        """
        Wraps the handler execution in a try-except block.

        Args:
            handler (Callable): Dialog event handler.
            event (TelegramObject): Incoming Telegram event.
            data (dict[str, Any]): Context data passed to the handler.

        Returns:
            Any: Result of the handler, or redirects to error dialog on failure.
        """
        try:
            return await handler(event, data)
        except Exception:
            logger.exception("Unhandled exception in dialog handler")
            logger.debug(event, exc_info=True)

            dialog_manager: DialogManager = cast(DialogManager, data.get("dialog_manager"))
            await dialog_manager.start(state=ErrorDialog.error, mode=StartMode.RESET_STACK)
