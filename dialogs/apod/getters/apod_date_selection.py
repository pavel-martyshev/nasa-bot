from datetime import datetime

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from config import app_settings


async def getter(dialog_manager: DialogManager, i18n: TranslatorRunner, language_code: str, **_):
    return {
        "incorrect_format_message": i18n.get("incorrect_format"),
        "incorrect_date_message": i18n.get("incorrect_date"),
        "date_request": i18n.get(
            "date_request",
            max_date=datetime.today().strftime(app_settings.get_date_format(language_code))
        ),
        "back_button_text": i18n.get("back"),
        "incorrect_format": dialog_manager.dialog_data.pop("incorrect_format", False),
        "incorrect_date": dialog_manager.dialog_data.pop("incorrect_date", False)
    }
