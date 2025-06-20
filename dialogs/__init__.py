from aiogram_dialog import Dialog

from dialogs.apod import apod_date_selection, apod_menu
from dialogs.error_dialog import error_window
from dialogs.info import info
from dialogs.main_menu import main_menu
from utils.middlewares.error_catching import SafeDialogMiddleware

error_dialog = Dialog(error_window)

info_dialog = Dialog(info)
info_dialog.callback_query.middleware(SafeDialogMiddleware())
info_dialog.message.middleware(SafeDialogMiddleware())

main_menu_dialog = Dialog(main_menu)
main_menu_dialog.callback_query.middleware(SafeDialogMiddleware())
main_menu_dialog.message.middleware(SafeDialogMiddleware())

apod_dialog = Dialog(apod_menu, apod_date_selection)
apod_dialog.callback_query.middleware(SafeDialogMiddleware())
apod_dialog.message.middleware(SafeDialogMiddleware())
