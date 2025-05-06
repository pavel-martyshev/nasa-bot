from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row, WebApp
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from dialogs.apod.getters.apod_menu import ApodProvider
from dialogs.apod.handlers.apod_menu import on_random_apod
from dialogs.common.widgets import back_to_main_menu
from states.states import APODSG

apod_menu = Window(
    DynamicMedia("resources", when=F["is_media_exist"]),
    Format("{apod_caption}", when=F["is_media_exist"]),
    Format("{media_not_exist_message}", when=~F["is_media_exist"]),
    SwitchTo(
        Format("{select_date_button_text}"),
        state=APODSG.apod_date_selection,
        id="apod_date_selection",
    ),
    Button(
        Format("{random_picture_button_text}"),
        on_click=on_random_apod,
        id="random_apod"
    ),
    Row(
        WebApp(
            text=Format("{explanation_button_text}"),
            url=Format("https://nasa-bot-web-app.ru?apod_id={apod_id}&language_code={language_code}"),
        ),
        back_to_main_menu,
    ),
    parse_mode="MARKDOWN",
    getter=ApodProvider(),
    state=APODSG.apod_menu
)
