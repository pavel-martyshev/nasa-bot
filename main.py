import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiogram_dialog.context.media_storage import MediaIdStorage
from fluentogram import TranslatorHub
from tortoise import Tortoise

from config import app_settings
from config.log_config import logger
from database.postgres.core import init_db
from database.redis import storage
from dialogs import apod_dialog, error_dialog, main_menu_dialog
from states.states import MainMenuSG
from utils.create_translator_hub import create_translator_hub
from utils.custom_dialog_manager import CustomDialogManager
from utils.custom_message_manager import CustomMessageManager
from utils.middlewares.i18n import TranslatorRunnerMiddleware
from utils.middlewares.user_activity_registration import UserActivityRegistrationMiddleware

bot = Bot(app_settings.token)
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(CommandStart())
async def root_handler(_message: Message, dialog_manager: DialogManager) -> None:
    """
    Handle /start command by launching the main menu dialog.

    Args:
        _message (Message): Incoming Telegram message (unused).
        dialog_manager (DialogManager): Dialog manager instance.
    """
    await dialog_manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


async def on_startup() -> None:
    """
    Executed when the bot starts. Logs the startup event.
    """
    logger.warning("Bot started")


async def on_shutdown() -> None:
    """
    Executed when the bot stops. Logs the shutdown event.
    """
    logger.warning("Bot stopped")


async def main() -> None:
    """
    Main entry point for the bot.

    Initializes the database, sets up middleware, dialogs, routers, and starts polling.
    """
    await init_db()
    await Tortoise.generate_schemas()

    translator_hub: TranslatorHub = create_translator_hub()
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(UserActivityRegistrationMiddleware())

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(error_dialog, main_menu_dialog, apod_dialog)
    setup_dialogs(
        dp,
        message_manager=CustomMessageManager(),
        dialog_manager_factory=CustomDialogManager(
            CustomMessageManager(),
            MediaIdStorage()  # type: ignore[no-untyped-call]
        )
    )

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, _translator_hub=translator_hub)


if __name__ == '__main__':
    asyncio.run(main())
