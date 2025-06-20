from aiogram_dialog import Window
from aiogram_dialog.widgets.text import Format

from dialogs.common.widgets.buttons.back_to_main_menu import back_to_main_menu
from dialogs.info.getters.info import getter
from states.states import InfoSG

info = Window(Format("{info}"), back_to_main_menu, getter=getter, state=InfoSG.info)
