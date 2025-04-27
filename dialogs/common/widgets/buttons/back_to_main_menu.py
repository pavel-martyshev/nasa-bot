from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from dialogs.texts import MAIN_MENU
from states import MainMenuSG

back_to_main_menu = Start(
    Const(MAIN_MENU),
    state=MainMenuSG.main_menu,
    mode=StartMode.RESET_STACK,
    id='back_to_main_menu',
)
