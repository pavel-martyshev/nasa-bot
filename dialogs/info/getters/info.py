import json
from pathlib import Path
from typing import Any

from fluentogram import TranslatorHub, TranslatorRunner

from config import app_settings


async def getter(
    language_code: str, i18n: TranslatorRunner, _translator_hub: TranslatorHub, **_: Any
) -> dict[str, str]:
    """
    Load localized APOD info text and main menu button label for the info dialog.

    Args:
        language_code (str): Language code (e.g., "en", "ru").
        i18n (TranslatorRunner): Translation runner for retrieving localized strings.
        _translator_hub (TranslatorHub): Translator hub used to verify supported languages.
        **_ (unused): Ignored extra arguments.

    Returns:
        dict[str, str]: Dictionary containing localized info text and main menu button label.
    """
    info_path = Path(app_settings.resources_path, "info", "info.json")

    with open(info_path, encoding="utf-8") as f:
        info = json.load(f)

    if language_code not in _translator_hub.locales_map.keys():
        language_code = "en"

    apod_info = info["apod"][language_code]

    return {"info": apod_info, "main_menu_button_text": i18n.get("back")}
