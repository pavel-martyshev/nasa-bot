from aiogram.types import CallbackQuery
from aiogram_dialog import DialogManager
from aiogram_dialog.widgets.kbd import Button


async def on_random_apod(_call: CallbackQuery, _widget: Button, dialog_manager: DialogManager) -> None:
    """
    Handle the 'random picture' button press by setting is_random flag.

    Args:
        _call (unused): Callback query from the button press.
        _widget (unused): Button widget instance.
        dialog_manager (DialogManager): Dialog manager to update dialog state.
    """
    dialog_manager.dialog_data.update(is_random=True)
