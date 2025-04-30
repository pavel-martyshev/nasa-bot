from datetime import datetime

from aiogram_dialog import DialogManager

from config import app_settings


async def getter(dialog_manager: DialogManager, **_):
    return {
        "incorrect_format": dialog_manager.dialog_data.pop("incorrect_format", False),
        "incorrect_date": dialog_manager.dialog_data.pop("incorrect_date", False),
        "max_date": datetime.today().strftime(app_settings.date_format),
    }
