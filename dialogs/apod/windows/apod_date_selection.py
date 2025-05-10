from aiogram import F
from aiogram.enums import ContentType, ParseMode
from aiogram_dialog import Window
from aiogram_dialog.widgets.input import MessageInput
from aiogram_dialog.widgets.kbd import Back
from aiogram_dialog.widgets.text import Format

from dialogs.apod.getters.apod_date_selection import getter
from dialogs.apod.handlers.apod_date_selection import handle_incorrect_message, handle_selected_date
from states.states import APODSG

apod_date_selection = Window(
    Format("{incorrect_format_message}" + "\n\n", when=F["incorrect_format"]),
    Format("{incorrect_date_message}" + "\n\n", when=F["incorrect_date"]),
    Format("{date_request}"),
    MessageInput(
        content_types=ContentType.TEXT,
        func=handle_selected_date,
    ),
    MessageInput(
        content_types=ContentType.ANY,
        func=handle_incorrect_message,
    ),
    Back(
        text=Format("{back_button_text}")
    ),
    parse_mode=ParseMode.MARKDOWN,
    getter=getter,
    state=APODSG.apod_date_selection
)
