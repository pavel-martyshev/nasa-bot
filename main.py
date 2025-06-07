import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram.webhook.aiohttp_server import SimpleRequestHandler, setup_application
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from aiogram_dialog.context.media_storage import MediaIdStorage
from aiohttp import web
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
from web_app_api.app import apod_explanation

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
    Executed when the bot starts. Logs the startup event. Initializes database. Sets webhook if it enabled.
    """
    await setup_database()

    if app_settings.api.is_webhook_enabled:
        await bot.set_webhook(
            url=str(app_settings.api.get_full_webhook_url()), secret_token=app_settings.api.webhook_key
        )

    logger.warning("Bot started")


async def on_shutdown() -> None:
    """
    Executed when the bot stops. Logs the shutdown event.
    """
    logger.warning("Bot stopped")


def get_webhook_app(i18n_hub: TranslatorHub) -> web.Application:
    """
    Create and configure an aiohttp web application with webhook handling.

    Args:
        i18n_hub (TranslatorHub): Instance managing translation logic and middleware.

    Returns:
        web.Application: Configured aiohttp app with routes and webhook support.
    """
    app = web.Application()
    app.add_routes([web.get("/apodExplanation", apod_explanation)])

    webhook_requests_handler = SimpleRequestHandler(
        dispatcher=dp,
        bot=bot,
        secret_token=app_settings.api.webhook_key,
        _translator_hub=i18n_hub,
    )
    webhook_requests_handler.register(app, path=f"/{app_settings.api.webhook_path}")

    setup_application(app, dp, bot=bot)

    return app


async def setup_database() -> None:
    """
    Initialize and apply database schema using Tortoise ORM.
    """
    await init_db()
    await Tortoise.generate_schemas()


def get_translator_hub() -> TranslatorHub:
    """
    Create and configure the translation hub and register global middlewares.

    Returns:
        TranslatorHub: Configured translation hub instance.
    """
    i18n_hub: TranslatorHub = create_translator_hub()
    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(UserActivityRegistrationMiddleware())

    return i18n_hub


def setup_dispatcher() -> None:
    """
    Register startup/shutdown hooks, include routers, and initialize dialog system.
    """
    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(error_dialog, main_menu_dialog, apod_dialog)

    setup_dialogs(
        dp,
        message_manager=CustomMessageManager(),
        dialog_manager_factory=CustomDialogManager(
            CustomMessageManager(),
            MediaIdStorage(),  # type: ignore[no-untyped-call]
        ),
    )


def run_webhook(i18n_hub: TranslatorHub) -> None:
    """
    Start the bot using aiohttp webhook server.

    Args:
        i18n_hub (TranslatorHub): Translation hub to inject into request handlers.
    """
    app: web.Application = get_webhook_app(i18n_hub)
    web.run_app(app, host=app_settings.api.webhook_host, port=app_settings.api.webhook_port)


async def run_polling(i18n_hub: TranslatorHub) -> None:
    """
    Start the bot using long polling.

    Args:
        i18n_hub (TranslatorHub): Translation hub to pass to dispatcher.
    """
    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot, _translator_hub=i18n_hub)


if __name__ == "__main__":
    translator_hub: TranslatorHub = get_translator_hub()
    setup_dispatcher()

    if app_settings.api.is_webhook_enabled:
        run_webhook(translator_hub)
    else:
        asyncio.run(run_polling(translator_hub))
