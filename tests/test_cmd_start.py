from collections.abc import AsyncGenerator
from datetime import datetime
from typing import Any

import pytest
from aiogram import Dispatcher
from aiogram.dispatcher.event.bases import UNHANDLED
from aiogram.methods import SendMessage, TelegramMethod
from aiogram.types import Chat, InlineKeyboardMarkup, Message, Update
from fluentogram import TranslatorHub

from tests.moks import BotMock
from tests.utils.factories.aiogram_factory import AiogramFactory


class TestCmdStart:
    @staticmethod
    async def _test_cmd_start(
            translator_hub: TranslatorHub,
            dp: Dispatcher,
            bot: BotMock,
            language_code: str = "en",
            outgoing_message_text: str = "Main menu",
            outgoing_button_text: str = "Picture of the day 🪐"
    ) -> None:
        chat: Chat = AiogramFactory.get_chat_instance()

        bot.add_result_for(
            method=SendMessage,
            ok=True,
            result=Message(
                message_id=1,
                date=datetime.now(),
                chat=chat
            )
        )

        message = Message(
            message_id=1,
            chat=chat,
            from_user=AiogramFactory.get_user_instance(user_id=chat.id, language_code=language_code),
            text="/start",
            date=datetime.now()
        )

        result = await dp.feed_update(
            bot,
            Update(message=message, update_id=1),
            _translator_hub=translator_hub
        )

        assert result is not UNHANDLED

        outgoing_message: TelegramMethod[Any] = bot.get_request()

        assert isinstance(outgoing_message, SendMessage)
        assert outgoing_message.text == outgoing_message_text
        assert isinstance(outgoing_message.reply_markup, InlineKeyboardMarkup)
        assert outgoing_message.reply_markup.inline_keyboard[0][0].text == outgoing_button_text
        assert outgoing_message.reply_markup.inline_keyboard[0][0].callback_data is not None
        assert "apod" in outgoing_message.reply_markup.inline_keyboard[0][0].callback_data

    @pytest.mark.asyncio
    async def test_cmd_start_ru(
            self,
            init_db: AsyncGenerator[None, Any],
            translator_hub: TranslatorHub,
            dispatcher: Dispatcher,
            bot: BotMock
    ) -> None:
        await self._test_cmd_start(
            translator_hub=translator_hub,
            dp=dispatcher,
            bot=bot,
            language_code="ru",
            outgoing_message_text="Главное меню",
            outgoing_button_text="Картинка дня 🪐"
        )

    @pytest.mark.asyncio
    async def test_cmd_start_en(
            self,
            init_db: AsyncGenerator[None, Any],
            translator_hub: TranslatorHub,
            dispatcher: Dispatcher,
            bot: BotMock
    ) -> None:
        await self._test_cmd_start(
            translator_hub=translator_hub,
            dp=dispatcher,
            bot=bot
        )

    @pytest.mark.asyncio
    async def test_cmd_start_de(
            self,
            init_db: AsyncGenerator[None, Any],
            translator_hub: TranslatorHub,
            dispatcher: Dispatcher,
            bot: BotMock
    ) -> None:
        await self._test_cmd_start(
            translator_hub=translator_hub,
            dp=dispatcher,
            bot=bot,
            language_code="de"
        )
