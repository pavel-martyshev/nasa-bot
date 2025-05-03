from datetime import datetime

from aiogram.types import Message
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.input import MessageInput

from config import app_settings
from states import APODSG


async def handle_selected_date(message: Message, _widget: MessageInput, dialog_manager: DialogManager):
    language_code: str = dialog_manager.middleware_data.get("language_code")

    try:
        date = datetime.strptime(
            message.text.replace(",", "."),
            app_settings.get_date_format(language_code)
        )
    except ValueError:
        return dialog_manager.dialog_data.update(incorrect_format=True)

    if date > datetime.now() or date < datetime(1995, 6, 16):
        return dialog_manager.dialog_data.update(incorrect_date=True)

    dialog_manager.dialog_data.update(apod_date=datetime.strftime(date, "%Y-%m-%d"))
    await dialog_manager.switch_to(APODSG.apod_menu)


async def handle_incorrect_message(_message: Message, _widget: MessageInput, dialog_manager: DialogManager):
    dialog_manager.dialog_data.update(incorrect_format=True)
