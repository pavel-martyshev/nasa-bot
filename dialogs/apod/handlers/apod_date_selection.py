from datetime import datetime
from typing import cast

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from config import app_settings
from config.log_config import logger
from states.states import APODSG


async def handle_selected_date(message: Message, _widget: MessageInput, dialog_manager: DialogManager) -> None:
    """
    Validate user-input date and update dialog state for APOD retrieval.

    Args:
        message (Message): Incoming Telegram message with user input.
        _widget (unused): Dialog widget reference.
        dialog_manager (DialogManager): Dialog manager for state and context.

    Raises:
        ValueError: If the message has no text.
    """
    language_code: str = cast(str, dialog_manager.middleware_data.get("language_code"))

    if not message.text:
        raise ValueError("Message text is empty")

    try:
        date = datetime.strptime(
            message.text.replace(",", ".").lstrip("\u2068").rstrip("\u2069"),
            app_settings.get_date_format(language_code),
        )
    except ValueError:
        logger.exception("Date formatting error")
        return dialog_manager.dialog_data.update(incorrect_format=True)

    if date > datetime.now() or date < datetime(1995, 6, 16):
        return dialog_manager.dialog_data.update(incorrect_date=True)

    dialog_manager.dialog_data.update(apod_date=datetime.strftime(date, "%Y-%m-%d"))
    await dialog_manager.switch_to(APODSG.apod_menu)


async def handle_invalid_input(_message: Message, _widget: MessageInput, dialog_manager: DialogManager) -> None:
    """
    Fallback handler that marks the user input as having incorrect format.

    Args:
        _message (unused): Incoming Telegram message.
        _widget (unused): Dialog widget reference.
        dialog_manager (DialogManager): Dialog manager to update dialog state.
    """
    dialog_manager.dialog_data.update(incorrect_format=True)
