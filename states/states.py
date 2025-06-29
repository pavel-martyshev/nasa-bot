from aiogram.fsm.state import State, StatesGroup


class ErrorDialog(StatesGroup):
    error = State()


class InfoSG(StatesGroup):
    info = State()


class MainMenuSG(StatesGroup):
    main_menu = State()


class APODSG(StatesGroup):
    apod_menu = State()
    apod_date_selection = State()
