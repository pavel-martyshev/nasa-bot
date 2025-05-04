from aiogram.fsm.state import StatesGroup, State


class ErrorDialog(StatesGroup):
    error = State()


class MainMenuSG(StatesGroup):
    main_menu = State()


class APODSG(StatesGroup):
    apod_menu = State()
    apod_date_selection = State()
