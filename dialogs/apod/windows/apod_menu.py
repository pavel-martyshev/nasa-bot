from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import Button, Row, SwitchTo, WebApp
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format

from config import app_settings
from dialogs.apod.getters.apod_menu import ApodProvider
from dialogs.apod.handlers.apod_menu import on_random_apod
from dialogs.common.widgets import back_to_main_menu
from states.states import APODSG

"""
Dialog window displaying the Astronomy Picture of the Day (APOD).

Includes media preview, caption, and buttons for:
- Selecting a specific date
- Requesting a random picture
- Opening a WebApp with explanation
- Returning to the main menu

State:
    APODSG.apod_menu
"""
apod_menu = Window(
    DynamicMedia("resources", when=~F["media_not_exist_message"]),
    Format("{apod_caption}", when=~F["media_not_exist_message"]),
    Format("{media_not_exist_message}", when=F["media_not_exist_message"]),
    SwitchTo(
        Format("{select_date_button_text}"),
        state=APODSG.apod_date_selection,
        id="apod_date_selection",
    ),
    Button(Format("{random_picture_button_text}"), on_click=on_random_apod, id="random_apod"),
    Row(
        WebApp(
            text=Format("{explanation_button_text}"),
            url=Format(app_settings.web_app_url),
            when=~F["media_not_exist_message"],
        ),
        back_to_main_menu,
    ),
    parse_mode="MARKDOWN",
    getter=ApodProvider(),
    state=APODSG.apod_menu,
)
