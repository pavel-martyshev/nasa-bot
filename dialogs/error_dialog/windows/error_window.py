from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from dialogs.common.widgets.buttons.back_to_main_menu import back_to_main_menu
from dialogs.error_dialog.getters.error_window import getter
from states import ErrorDialog

error_window = Window(
    Format("{unexpected_error_message}"),
    back_to_main_menu,
    getter=getter,
    state=ErrorDialog.error
)
