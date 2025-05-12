from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from dialogs.common.widgets.buttons.back_to_main_menu import back_to_main_menu
from dialogs.error_dialog.getters.error_window import getter
from states.states import ErrorDialog

"""
Fallback error dialog shown when an unexpected exception occurs.

Provides a localized error message and a button to return to the main menu.
Used as a safety net to ensure the bot remains responsive.

State:
    ErrorDialog.error
"""
error_window = Window(
    Format("{unexpected_error_message}"),
    back_to_main_menu,
    getter=getter,
    state=ErrorDialog.error
)
