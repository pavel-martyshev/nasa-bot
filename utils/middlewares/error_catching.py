from collections.abc import Awaitable
from typing import Any, Callable, cast

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import DialogManager, StartMode

from config.log_config import logger
from states.states import ErrorDialog


class ErrorCatchingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: dict[str, Any]
    ) -> Any:
        try:
            return await handler(event, data)
        except Exception:
            logger.exception("Unhandled exception in dialog handler")

            dialog_manager: DialogManager = cast(DialogManager, data.get("dialog_manager"))
            await dialog_manager.start(state=ErrorDialog.error, mode=StartMode.RESET_STACK)
