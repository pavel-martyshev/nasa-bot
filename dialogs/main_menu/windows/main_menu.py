from aiogram_dialog import Window, StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format

from dialogs.main_menu.getters.main_menu import getter
from states import MainMenuSG, APODSG

main_menu = Window(
    Format("{main_menu_text}"),
    Start(
        Format("{apod_button_text}"),
        state=APODSG.apod_menu,
        mode=StartMode.RESET_STACK,
        id="apod"
    ),
    getter=getter,
    state=MainMenuSG.main_menu
)
