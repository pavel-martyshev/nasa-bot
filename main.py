import asyncio

from aiogram import Bot, Dispatcher, F
from aiogram.filters import CommandStart
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from tortoise import Tortoise

from config import app_settings
from config.log_config import logger
from database.postgres.core import init_db
from database.redis import storage
from dialogs import apod_dialog, main_menu_dialog
from states import MainMenuSG

bot = Bot(app_settings.token)
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(CommandStart())
async def root_handler(message: Message, dialog_manager: DialogManager):
    app_settings.language_code = message.from_user.language_code

    await dialog_manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


@dp.message(F.web_app_data)
async def handle_web_app_data(message: Message):
    data = message.web_app_data.data
    await message.answer(f"Принятые данные из мини-приложения: {data}")


async def on_startup():
    """
    Function to be executed on bot startup.
    Logs the start of the bot.
    """
    logger.warning("Bot started")


async def on_shutdown():
    """
    Function to be executed on bot shutdown.
    Logs the stop of the bot.
    """
    logger.warning("Bot stopped")


async def main():
    await init_db()
    await Tortoise.generate_schemas()

    dp.startup.register(on_startup)
    dp.shutdown.register(on_shutdown)

    dp.include_routers(main_menu_dialog, apod_dialog)
    setup_dialogs(dp)

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
