from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from dialogs.common.widgets.buttons.back_to_main_menu import back_to_main_menu
from states import APODSG

unexpected_error = Window(
    Format("unexpected_error_message"),
    back_to_main_menu,
    state=APODSG.unexpected_error
)
