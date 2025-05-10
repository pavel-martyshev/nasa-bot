from typing import Any

from fluentogram import TranslatorRunner


async def getter(i18n: TranslatorRunner, **_: dict[str, Any]) -> dict[str, str]:
    return {"main_menu_text": i18n.get("main_menu"), "apod_button_text": i18n.get("apod_button")}
