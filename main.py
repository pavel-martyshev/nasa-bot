import asyncio

from aiogram import Bot, Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from aiogram.methods import DeleteWebhook
from aiogram.types import Message
from aiogram_dialog import DialogManager, StartMode, setup_dialogs
from icecream import ic
from redis.asyncio import Redis

from config import app_config
from dialogs import apod_dialog, main_menu_dialog
from states import MainMenuSG

redis = Redis()
storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(prefix="nasa-bot", with_destiny=True))

bot = Bot(app_config.token)
dp = Dispatcher(bot=bot, storage=storage)


@dp.message(CommandStart())
async def root_handler(message: Message, dialog_manager: DialogManager):
    await dialog_manager.start(MainMenuSG.main_menu, mode=StartMode.RESET_STACK)


async def _on_startup() -> None:
    """
    Function to be executed on bot startup.
    Logs the start of the bot.
    """
    # logger.warning("Bot started")
    ic('Bot started')


async def _on_shutdown() -> None:
    """
    Function to be executed on bot shutdown.
    Logs the stop of the bot.
    """
    # logger.warning("Bot stopped")
    from icecream import ic
    ic('Bot stopped')


async def main():
    dp.startup.register(_on_startup)
    dp.shutdown.register(_on_shutdown)

    dp.include_routers(main_menu_dialog, apod_dialog)
    setup_dialogs(dp)

    await bot(DeleteWebhook(drop_pending_updates=True))
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
