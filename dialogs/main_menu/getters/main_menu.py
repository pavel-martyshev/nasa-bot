from fluentogram import TranslatorRunner


async def getter(i18n: TranslatorRunner, **_):
    return {"main_menu_text": i18n.get("main_menu"), "apod_button_text": i18n.get("apod_button")}
