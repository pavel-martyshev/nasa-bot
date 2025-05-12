from typing import Any

from fluentogram import TranslatorRunner


async def getter(i18n: TranslatorRunner, **_: dict[str, Any]) -> dict[str, str]:
    """
    Provide localized text for the main menu window.

    Args:
        i18n (TranslatorRunner): Translation provider.
        **_ (unused): Ignored extra arguments.

    Returns:
        dict[str, str]: Localized main menu message and APOD button text.
    """
    return {"main_menu_text": i18n.get("main_menu"), "apod_button_text": i18n.get("apod_button")}
