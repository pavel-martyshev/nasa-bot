from fluentogram import TranslatorRunner


async def getter(i18n: TranslatorRunner, **_):
    return {
        "unexpected_error_message": i18n.get("unexpected_error"),
        "main_menu_button_text": i18n.get("main_menu")
    }
