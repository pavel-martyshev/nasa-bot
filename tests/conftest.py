import sys
from collections.abc import AsyncGenerator
from pathlib import Path
from typing import Any

import pytest
import pytest_asyncio
from aiogram import Dispatcher
from aiogram.filters import CommandStart
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram_dialog import setup_dialogs
from aiogram_dialog.context.media_storage import MediaIdStorage
from fluent_compiler.bundle import FluentBundle
from fluentogram import FluentTranslator, TranslatorHub
from tortoise import Tortoise

from main import root_handler
from tests.moks import BotMock, SessionMock
from tests.utils.factories.dialogs_factory import DialogsFactory
from utils.custom_dialog_manager import CustomDialogManager
from utils.custom_message_manager import CustomMessageManager
from utils.middlewares.i18n import TranslatorRunnerMiddleware
from utils.middlewares.user_activity_registration import UserActivityRegistrationMiddleware

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))


@pytest_asyncio.fixture(scope="function", autouse=True)
async def init_db() -> AsyncGenerator[Any, None]:
    await Tortoise.init(
        db_url="sqlite://:memory:",
        modules={"models": [
            "database.postgres.models.apod",
            "database.postgres.models.user",
        ]}
    )
    await Tortoise.generate_schemas()

    yield

    await Tortoise._drop_databases()


@pytest.fixture(scope="function", autouse=True)
def translator_hub() -> TranslatorHub:
    source_path = Path(__file__).parent.parent
    ru_locales_path = source_path.joinpath(*("locales", "ru", "LC_MESSAGES", "txt.ftl"))
    en_locales_path = source_path.joinpath(*("locales", "en", "LC_MESSAGES", "txt.ftl"))

    translator_hub = TranslatorHub(
        {
            "ru": ("ru", "en"),
            "en": ("en", "ru")
        },
        [
            FluentTranslator(
                locale="ru",
                translator=FluentBundle.from_files(
                    locale="ru-RU",
                    filenames=[ru_locales_path])),
            FluentTranslator(
                locale="en",
                translator=FluentBundle.from_files(
                    locale="en-US",
                    filenames=[en_locales_path]))
        ],
    )

    return translator_hub


@pytest.fixture(scope="function", autouse=True)
def dispatcher() -> Dispatcher:
    dp = Dispatcher(storage=MemoryStorage())

    dp.update.middleware(TranslatorRunnerMiddleware())
    dp.update.middleware(UserActivityRegistrationMiddleware())

    dp.message.register(root_handler, CommandStart())
    dp.include_routers(
        DialogsFactory.get_apod_dialog(),
        DialogsFactory.get_main_menu_dialog(),
        DialogsFactory.get_error_dialog()
    )

    setup_dialogs(
        dp,
        message_manager=CustomMessageManager(),
        dialog_manager_factory=CustomDialogManager(
            CustomMessageManager(),
            MediaIdStorage()  # type: ignore[no-untyped-call]
        )
    )

    return dp


@pytest.fixture(scope="function", autouse=True)
def bot() -> BotMock:
    bot = BotMock()
    bot.session = SessionMock()
    return bot
