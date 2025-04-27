from aiogram_dialog import DialogManager


async def getter(dialog_manager: DialogManager, **_):
    return {"incorrect_format": dialog_manager.dialog_data.pop("incorrect_format", False)}
