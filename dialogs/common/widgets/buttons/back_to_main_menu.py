from aiogram_dialog import StartMode
from aiogram_dialog.widgets.kbd import Start
from aiogram_dialog.widgets.text import Format

from states import MainMenuSG

back_to_main_menu = Start(
    Format("{main_menu_button_text}"),
    state=MainMenuSG.main_menu,
    mode=StartMode.RESET_STACK,
    id='back_to_main_menu',
)
