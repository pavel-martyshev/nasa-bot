from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.text import Const

from dialogs.apod.getters.apod_date_selection import getter
from dialogs.apod.handlers.apod_date_selection import handle_selected_date, handle_incorrect_message
from dialogs.apod.texts import DATE_REQUEST
from dialogs.texts import INCORRECT_FORMAT
from states import APODSG

apod_date_selection = Window(
    Const(INCORRECT_FORMAT + "\n", when=F["incorrect_format"]),
    Const(DATE_REQUEST),
    MessageInput(
        content_types=ContentType.TEXT,
        func=handle_selected_date,
    ),
    MessageInput(
        content_types=ContentType.ANY,
        func=handle_incorrect_message,
    ),
    parse_mode=ParseMode.MARKDOWN,
    getter=getter,
    state=APODSG.apod_date_selection
)
