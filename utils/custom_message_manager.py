import re
from datetime import datetime

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import Message
from aiogram_dialog.api.entities import NewMessage, OldMessage
from aiogram_dialog.manager.message_manager import SEND_METHODS, MessageManager, INPUT_MEDIA_TYPES
from babel.dates import format_date

from config.log_config import logger
from database.postgres.core.CRUD.apod import APODCRUD

_DATE_PATTERN = r"\d{4}-\d{2}-\d{2}"


class CustomMessageManager(MessageManager):
    __language_code: str
    __apod_crud: APODCRUD = APODCRUD()

    def __init__(self):
        super().__init__()
        self.__language_code = "en"

    @property
    def language_code(self):
        return self.__language_code

    @language_code.setter
    def language_code(self, value):
        self.__language_code = value

    async def __save_file_id(self, message: Message, date: datetime):
        media_content_type = message.content_type

        if media_content_type == ContentType.PHOTO:
            file_id = message.photo[-1].file_id
        else:
            file_id = getattr(message, media_content_type).file_id

        if not await  self.__apod_crud.exists(file_id=file_id):
            await self.__apod_crud.update(filters={"date": date}, file_id=file_id)
            logger.debug(f"Saved file_id for date {date.strftime('%Y-%m-%d')}")

    def __get_date_with_formatting_date_caption(self, text: str) -> (datetime, str):
        date_string = re.search(_DATE_PATTERN, text).group()
        date = datetime.strptime(date_string, "%Y-%m-%d")

        return date, re.sub(_DATE_PATTERN, format_date(date, format="long", locale=self.__language_code), text)

    async def send_media(self, bot: Bot, new_message: NewMessage) -> Message:
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

        await self.__save_file_id(media_message, date)

        return media_message

    async def edit_media(
            self, bot: Bot, new_message: NewMessage, old_message: OldMessage,
    ) -> Message:
        logger.debug(
            "edit_media to %s, media_id: %s",
            new_message.chat,
            new_message.media.file_id,
        )

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
            reply_markup=new_message.reply_markup,
        )

        await self.__save_file_id(media_message, date)

        return media_message
