from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Const

from dialogs.main_menu.texts import APOD
from dialogs.texts import MAIN_MENU
from states import MainMenuSG, APODSG

main_menu = Window(
    Const(MAIN_MENU),
    Start(
        Const(APOD),
        state=APODSG.apod_menu,
        mode=StartMode.RESET_STACK,
        id="apod"
    ),
    state=MainMenuSG.main_menu
)
