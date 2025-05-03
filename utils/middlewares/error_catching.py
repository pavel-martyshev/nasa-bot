from typing import Callable, Dict, Any, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import TelegramObject
from aiogram_dialog import DialogManager, StartMode

from config.log_config import logger
from states import ErrorDialog


class ErrorCatchingMiddleware(BaseMiddleware):
    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any]
    ):
        try:
            return await handler(event, data)
        except Exception:
            logger.exception("Unhandled exception in dialog handler")

            dialog_manager: DialogManager = data.get("dialog_manager")
            await dialog_manager.start(state=ErrorDialog.error, mode=StartMode.RESET_STACK)
