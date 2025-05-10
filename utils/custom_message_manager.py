import re
from datetime import datetime
from typing import cast

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import InlineKeyboardMarkup, Message
from aiogram_dialog.api.entities import NewMessage, OldMessage
from aiogram_dialog.manager.message_manager import INPUT_MEDIA_TYPES, SEND_METHODS, MessageManager
from babel.dates import format_date

from config.log_config import logger
from database.postgres.core.CRUD.apod import APODCRUD

_DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"


class CustomMessageManager(MessageManager):
    __language_code: str
    __apod_crud: APODCRUD = APODCRUD()

    def __init__(self) -> None:
        super().__init__()
        self.__language_code = "en"

    @property
    def language_code(self) -> str:
        return self.__language_code

    @language_code.setter
    def language_code(self, value: str) -> None:
        self.__language_code = value

    async def __save_file_id(self, message: Message, date: datetime) -> None:
        media_content_type = message.content_type

        if media_content_type == ContentType.PHOTO:
            if not message.photo:
                raise ValueError("Photo is None")

            file_id = message.photo[-1].file_id
        else:
            file_id = getattr(message, media_content_type).file_id

        if not await  self.__apod_crud.exists(file_id=file_id):
            await self.__apod_crud.update(filters={"date": date}, file_id=file_id)
            logger.debug(f"Saved file_id for date {date.strftime('%Y-%m-%d')}")

    def __get_date_with_formatting_date_caption(self, text: str) -> tuple[datetime, str]:
        match = re.search(_DATE_PATTERN, text)

        if not match:
            raise ValueError("Date format is invalid")

        date = datetime.strptime(match.group(), "%Y-%m-%d")

        return date, re.sub(_DATE_PATTERN, format_date(date, format="long", locale=self.__language_code), text)

    async def send_media(self, bot: Bot, new_message: NewMessage) -> Message:
        if not new_message.media:
            raise ValueError("There is no media in the message.")

        logger.debug(
            "send_media to %s, media_id: %s",
            new_message.chat,
            new_message.media.file_id,
        )
        method = getattr(bot, SEND_METHODS[new_message.media.type], None)
        if not method:
            raise ValueError(
                f"ContentType {new_message.media.type} is not supported",
            )

        date = None
        caption: str | None = new_message.text

        if new_message.text:
            date, caption = self.__get_date_with_formatting_date_caption(new_message.text)

        media_message: Message = await method(
            new_message.chat.id,
            await self.get_media_source(new_message.media, bot),
            message_thread_id=new_message.thread_id,
            business_connection_id=new_message.business_connection_id,
            caption=caption,
            reply_markup=new_message.reply_markup,
            parse_mode=new_message.parse_mode,
            **new_message.media.kwargs,
        )

        if date:
            await self.__save_file_id(media_message, date)

        return media_message

    async def edit_media(
            self, bot: Bot, new_message: NewMessage, old_message: OldMessage,
    ) -> Message:
        if not new_message.media:
            raise ValueError("There is no media in the message.")

        logger.debug(
            "edit_media to %s, media_id: %s",
            new_message.chat,
            new_message.media.file_id,
        )

        date = None
        caption: str | None = new_message.text

        if new_message.text:
            date, caption = self.__get_date_with_formatting_date_caption(new_message.text)

        media = INPUT_MEDIA_TYPES[new_message.media.type](
            caption=caption,
            reply_markup=new_message.reply_markup,
            parse_mode=new_message.parse_mode,
            media=await self.get_media_source(new_message.media, bot),
            **new_message.media.kwargs,
        )

        media_message = await bot.edit_message_media(
            message_id=old_message.message_id,
            chat_id=old_message.chat.id,
            media=media,
            reply_markup=cast(InlineKeyboardMarkup, new_message.reply_markup),
        )

        assert isinstance(media_message, Message)

        if date:
            await self.__save_file_id(media_message, date)

        return media_message
