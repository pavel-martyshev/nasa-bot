from typing import Any

from fluentogram import TranslatorRunner


async def getter(i18n: TranslatorRunner, **_: dict[str, Any]) -> dict[str, str]:
    return {
        "unexpected_error_message": i18n.get("unexpected_error"),
        "main_menu_button_text": i18n.get("main_menu")
    }
