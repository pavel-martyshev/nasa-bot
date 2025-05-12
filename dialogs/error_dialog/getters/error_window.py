from typing import Any

from fluentogram import TranslatorRunner


async def getter(i18n: TranslatorRunner, **_: dict[str, Any]) -> dict[str, str]:
    """
    Prepare localized strings for the fallback error window.

    Args:
        i18n (TranslatorRunner): Translation provider.
        **_ (unused): Ignored extra arguments.

    Returns:
        dict[str, str]: Dictionary with localized error message and button text.
    """
    return {
        "unexpected_error_message": i18n.get("unexpected_error"),
        "main_menu_button_text": i18n.get("main_menu")
    }
