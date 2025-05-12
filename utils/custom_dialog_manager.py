from typing import Any

from aiogram import Router
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import ChatEvent
from aiogram_dialog.api.protocols import DialogRegistryProtocol, MediaIdStorageProtocol
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.manager.manager_factory import DefaultManagerFactory

from utils.custom_message_manager import CustomMessageManager


class CustomDialogManager(DefaultManagerFactory):
    """
    Custom dialog manager factory that injects language code into the message manager.

    Extends DefaultManagerFactory to customize dialog behavior per language.
    """
    def __init__(
            self,
            message_manager: CustomMessageManager,
            media_id_storage: MediaIdStorageProtocol,
    ):
        super().__init__(
            message_manager,
            media_id_storage
        )

    def __call__(
            self,
            event: ChatEvent,
            data: dict[str, Any],
            registry: DialogRegistryProtocol,
            router: Router,
    ) -> DialogManager:
        """
        Create a DialogManager instance with injected language-aware message manager.

        Args:
            event (ChatEvent): Incoming chat event.
            data (dict[str, Any]): Contextual data, must include 'language_code'.
            registry (DialogRegistryProtocol): Dialog registry.
            router (Router): Bot router instance.

        Returns:
            DialogManager: Initialized dialog manager with localization support.
        """
        self.message_manager.language_code = data["language_code"]  # type: ignore[attr-defined]

        return ManagerImpl(
            event=event,
            data=data,
            message_manager=self.message_manager,
            media_id_storage=self.media_id_storage,
            registry=registry,
            router=router,
        )
