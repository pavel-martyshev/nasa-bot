from copy import deepcopy
from typing import Any
from unittest.mock import MagicMock

from aiogram_dialog import DialogManager


class DialogManagerFactory:
    _dialog_manager = MagicMock(spec=DialogManager)

    def __init__(self, dialog_data: dict[str, Any]):
        self._dialog_manager.dialog_data = dialog_data

    @property
    def dialog_manager(self) -> MagicMock:
        return deepcopy(self._dialog_manager)
