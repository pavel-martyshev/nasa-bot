from aiogram import F
from aiogram_dialog import Window
from aiogram_dialog.widgets.kbd import SwitchTo, Button, Row, WebApp
from aiogram_dialog.widgets.media import DynamicMedia
from aiogram_dialog.widgets.text import Format, Const

from dialogs.apod.getters.apod_menu import ApodProvider
from dialogs.apod.handlers.apod_menu import on_random_apod
from dialogs.apod.texts import DATE_SELECTION, RANDOM_APOD, APOD_CAPTION, MEDIA_NOT_EXIST
from dialogs.common.widgets import back_to_main_menu
from states import APODSG

apod_menu = Window(
    DynamicMedia("media", when=F["is_media_exist"]),
    Format(APOD_CAPTION, when=F["is_media_exist"]),
    Format(MEDIA_NOT_EXIST, when=~F["is_media_exist"]),
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
    WebApp(
        text=Const("Описание"),
        url=Format("https://chatty-rules-make.loca.lt?apod_id={apod_id}&language_code={language_code}"),
    ),
    back_to_main_menu,
    parse_mode="MARKDOWN",
    getter=ApodProvider(),
    state=APODSG.apod_menu
)
