from datetime import datetime
from typing import Any

from aiogram_dialog import DialogManager
from fluentogram import TranslatorRunner

from config import app_settings


async def getter(dialog_manager: DialogManager, i18n: TranslatorRunner, language_code: str, **_: Any) -> dict[str, Any]:
    """
    Prepare localized data for rendering a dialog step.

    Args:
        dialog_manager (DialogManager): Manages dialog state and context.
        i18n (TranslatorRunner): Translator for localized text.
        language_code (str): Current user language.
        **_ (unused): Ignored additional arguments.

    Returns:
        dict[str, Any]: Dictionary with localized strings for the UI, including optional error messages.
    """
    result = {
        "date_request": i18n.get(
            "date_request",
            max_date=datetime.today().strftime(app_settings.get_date_format(language_code))
        ),
        "back_button_text": i18n.get("back"),
    }

    if dialog_manager.dialog_data.pop("incorrect_format", False):
        result |= {"incorrect_format_message": i18n.get("incorrect_format")}
    elif dialog_manager.dialog_data.pop("incorrect_date", False):
        result |= {"incorrect_date_message": i18n.get("incorrect_date")}

    return result
