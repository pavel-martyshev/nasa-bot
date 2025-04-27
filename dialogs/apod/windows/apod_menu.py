from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from dialogs.apod.getters.apod_menu import getter
from dialogs.apod.handlers.apod_menu import on_random_apod
from dialogs.apod.texts import DATE_SELECTION, RANDOM_APOD
from dialogs.common.widgets import back_to_main_menu
from states import APODSG

apod_menu = Window(
    DynamicMedia("media", when=F["media"]),
    Format("Дата: {date}\n", when=F["date"]),
    Format("{explanation}", when=F["explanation"]),
    Row(
        SwitchTo(
            Const(DATE_SELECTION),
            state=APODSG.apod_date_selection,
            id="apod_date_selection",
        ),
        Button(
            Const(RANDOM_APOD),
            on_click=on_random_apod,
            id="random_apod"
        )
    ),
    back_to_main_menu,
    getter=getter,
    state=APODSG.apod_menu
)
