from aiogram_dialog import Dialog

from dialogs.error_dialog.windows.error_window import error_window
from dialogs.main_menu import main_menu
from dialogs.apod import apod_menu, apod_date_selection
from utils.middlewares.error_catching import ErrorCatchingMiddleware

error_dialog = Dialog(
    error_window
)

main_menu_dialog = Dialog(
    main_menu
)
main_menu_dialog.callback_query.middleware(ErrorCatchingMiddleware())
main_menu_dialog.message.middleware(ErrorCatchingMiddleware())

apod_dialog = Dialog(
    apod_menu,
    apod_date_selection
)
apod_dialog.callback_query.middleware(ErrorCatchingMiddleware())
apod_dialog.message.middleware(ErrorCatchingMiddleware())
