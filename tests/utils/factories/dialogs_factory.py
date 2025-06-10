from aiogram_dialog import Dialog

from dialogs.apod import apod_date_selection, apod_menu
from dialogs.error_dialog import error_window
from dialogs.main_menu import main_menu


class DialogsFactory:
    @staticmethod
    def get_error_dialog() -> Dialog:
        return Dialog(error_window)

    @staticmethod
    def get_main_menu_dialog() -> Dialog:
        return Dialog(main_menu)

    @staticmethod
    def get_apod_dialog() -> Dialog:
        return Dialog(apod_menu, apod_date_selection)
