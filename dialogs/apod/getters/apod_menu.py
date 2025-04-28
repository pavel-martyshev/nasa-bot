from datetime import datetime
from typing import Dict, Union

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment
import yt_dlp
from icecream import ic
from yt_dlp import DownloadError

from config import app_config
from http_client.aiohttp_client import HttpClient


class ApodProvider:
    __apod_url_part = f"/planetary/apod?api_key={app_config.nasa_api_key}"

    async def __get_apod_url(self, dialog_manager: DialogManager) -> str:
        url: str = app_config.nasa_api_base_url + self.__apod_url_part

        if dialog_manager.dialog_data.get("apod_date"):
            url += f"&date={dialog_manager.dialog_data.pop('apod_date')}"
        elif dialog_manager.dialog_data.pop("random_apod", False):
            url += f"&count=1"

        return url

    @staticmethod
    async def __get_apod_media(apod_data: Dict[str, str]) -> Union[MediaAttachment, None]:
        if apod_data["media_type"] == "image":
            media = MediaAttachment(ContentType.PHOTO, apod_data["url"])
        else:
            ydl_opts = {
                'format': 'best',
                'quiet': True,
            }

            try:
                with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(apod_data["url"], download=False)
                    media = MediaAttachment(ContentType.VIDEO, info.get("url", None))
            except DownloadError:
                media = None

        return media

    @staticmethod
    async def __get_formatted_date(date: str, language_code: str) -> str:
        if language_code == "ru":
            return datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%d.%m.%Y")

        if language_code == "en":
            return datetime.strftime(datetime.strptime(date, "%Y-%m-%d"), "%d/%m/%Y")

        return date

    async def __call__(self, event_from_user: User, dialog_manager: DialogManager, bot: Bot, **_):
        apod_url = await self.__get_apod_url(dialog_manager)

        apod_data = await HttpClient.get_apod(url=apod_url)

        if isinstance(apod_data, list):
            apod_data = apod_data[0]

        media = await self.__get_apod_media(apod_data)

        return {
            "date": await self.__get_formatted_date(apod_data["date"], event_from_user.language_code),
            "is_media_exist": bool(media),
            "media": media
        }
