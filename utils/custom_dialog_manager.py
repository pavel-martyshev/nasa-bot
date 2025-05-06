from aiogram import Router
from aiogram_dialog import DialogManager
from aiogram_dialog.api.protocols import MediaIdStorageProtocol, DialogRegistryProtocol
from aiogram_dialog.manager.manager import ManagerImpl
from aiogram_dialog.api.entities import ChatEvent
from aiogram_dialog.manager.manager_factory import DefaultManagerFactory

from utils.custom_message_manager import CustomMessageManager


class CustomDialogManager(DefaultManagerFactory):
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
            self, event: ChatEvent, data: dict,
            registry: DialogRegistryProtocol,
            router: Router,
    ) -> DialogManager:
        self.message_manager.language_code = data["language_code"]

        return ManagerImpl(
            event=event,
            data=data,
            message_manager=self.message_manager,
            media_id_storage=self.media_id_storage,
            registry=registry,
            router=router,
        )
