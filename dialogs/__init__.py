from aiogram_dialog import Dialog

from dialogs.main_menu import main_menu
from dialogs.apod import apod_menu, apod_date_selection

main_menu_dialog = Dialog(
    main_menu
)

apod_dialog = Dialog(
    apod_menu,
    apod_date_selection
)
