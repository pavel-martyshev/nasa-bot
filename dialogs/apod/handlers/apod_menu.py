from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def on_random_apod(_call: CallbackQuery, _widget: Button, dialog_manager: DialogManager) -> None:
    dialog_manager.dialog_data.update(is_random=True)
