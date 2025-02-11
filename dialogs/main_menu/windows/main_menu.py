from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Const

from dialogs.main_menu.texts import MAIN_MENU

main_menu = Window(
    Const(MAIN_MENU),
    state
)
