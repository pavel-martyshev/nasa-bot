from datetime import datetime
from typing import Dict, Union, Any

from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
import yt_dlp
from fluentogram import TranslatorRunner
from tortoise.contrib.pydantic import PydanticModel
from yarl import URL
from yt_dlp import DownloadError

from config import app_settings
from config.log_config import log_return_value, logger
from database.postgres.core.CRUD.APOD import APODCRUD
from http_client.aiohttp_client import HttpClient


class ApodProvider:
    __apod_url_parts: (str, str) = "planetary", "apod"
    __apod_crud: APODCRUD = APODCRUD()

    @log_return_value
    async def __get_apod_url(self, apod_date: str | None, is_random: bool) -> URL:
        query_params = {"api_key": app_settings.api.nasa_api_key}

        if apod_date:
            query_params["date"] = apod_date
        elif is_random:
            query_params["count"] = 1

        return app_settings.api.build_url(*self.__apod_url_parts, **query_params)

    @staticmethod
    async def __get_apod_media(media_type: str, media_url: str, apod_date: str) -> Union[MediaAttachment, None]:
        logger.info(f"APOD url at {apod_date}: {media_url}")

        if media_type == "image":
            media = MediaAttachment(ContentType.PHOTO, media_url)
        else:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(media_url, download=False)
                    media = MediaAttachment(ContentType.VIDEO, info.get("url", None))
            except DownloadError:
                media = None

        return media

    @staticmethod
    async def __prepare_payload(data: Dict[str, Any]) -> Dict[str, Any]:
        data.pop("copyright", None)
        data.pop("service_version", None)

        translated_texts = (await HttpClient.translate(texts=[data["title"], data["explanation"]]))["translations"]

        data["title_ru"] = translated_texts[0]["text"]
        data["explanation_ru"] = translated_texts[1]["text"]

        return data

    async def __get_apod_data(self, apod_date: str | None, is_random: bool) -> Dict[str, Any]:
        apod_json: Dict[str, Any] = await HttpClient.get(url=await self.__get_apod_url(apod_date, is_random))

        if isinstance(apod_json, list):
            apod_json = apod_json[0]

        return await self.__prepare_payload(apod_json)

    async def __call__(self,
                       event_from_user: User,
                       dialog_manager: DialogManager,
                       i18n: TranslatorRunner,
                       language_code: str,
                       **_):
        apod_date = dialog_manager.dialog_data.pop("apod_date", None)
        is_random = dialog_manager.dialog_data.pop("is_random", False)

        if not apod_date and not is_random:
            apod_date = datetime.today().strftime("%Y-%m-%d")

        apod: PydanticModel | None= await self.__apod_crud.get_apod(date=apod_date)

        if apod:
            media = await self.__get_apod_media(apod.media_type, apod.url, apod.date)
        else:
            apod_data: Dict[str, Any] = await self.__get_apod_data(apod_date=apod_date, is_random=is_random)
            apod: PydanticModel = await self.__apod_crud.get_or_create(**apod_data)

            media = await self.__get_apod_media(apod.media_type, apod.url, apod.date)

        return {
            "apod_caption": i18n.get(
                "apod_caption",
                date=apod.date,
                title=apod.title_ru if language_code == "ru" else apod.title
            ),
            "media_not_exist_message": i18n.get("media_not_exist"),
            "select_date_button_text": i18n.get("select_date"),
            "random_picture_button_text": i18n.get("random_picture"),
            "explanation_button_text": i18n.get("explanation"),
            "main_menu_button_text": i18n.get("main_menu"),
            "is_media_exist": bool(media),
            "media": media,
            "apod_id": apod.id,
            "language_code": language_code,
        }
