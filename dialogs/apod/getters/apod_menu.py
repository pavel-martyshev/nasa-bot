from datetime import datetime
from pathlib import Path
from typing import Any, Union, cast

from aiogram import Bot
from aiogram.enums import ChatAction, ContentType
from aiogram.types import CallbackQuery, Message
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from fluentogram import TranslatorRunner
from yarl import URL
from yt_dlp import DownloadError, YoutubeDL

from config import app_settings
from config.log_config import log_return_value, logger
from database.postgres.core.CRUD.apod import ApodCrud
from database.postgres.core.protocols import ApodProtocol
from utils.enums.apod_content_type import ApodContentType
from utils.http_client import HttpClient


class ApodProvider:
    """
    Fetches and prepares NASA APOD data for dialog rendering.

    Handles media download, translation, and caption formatting.
    """

    __apod_url_parts: tuple[str, str] = "planetary", "apod"
    __apod_crud: ApodCrud = ApodCrud()

    @log_return_value
    def __get_apod_url(self, apod_date: str | None, is_random: bool) -> URL:
        """
        Build NASA APOD API URL with optional date or random image query.

        Args:
            apod_date (str | None): Specific date for the APOD request.
            is_random (bool): Whether to fetch a random APOD.

        Returns:
            URL: Fully constructed request URL.
        """
        query_params = {"api_key": app_settings.api.nasa_api_key}

        if apod_date:
            query_params["date"] = apod_date
        elif is_random:
            query_params["count"] = "1"

        return app_settings.api.build_nasa_url(*self.__apod_url_parts, **query_params)

    @staticmethod
    async def __get_apod_media(media_type: str, media_url: str, apod_date: str) -> Union[MediaAttachment, None]:
        """
        Download APOD media and wrap it as a MediaAttachment.

        Args:
            media_type (str): Type of media ("image" or "video").
            media_url (str): URL to the media resource.
            apod_date (str): Date of the APOD (used for logging).

        Returns:
            MediaAttachment | None: Wrapped media, or None if download failed.
        """
        logger.info(f"APOD url at {apod_date}: {media_url}")

        if media_type == "image":
            media = MediaAttachment(ContentType.PHOTO, media_url)
        else:
            ydl_opts = {
                "format": "best[ext=mp4]/best",
                "outtmpl": str(Path(app_settings.get_full_temp_path(), "%(title)s.%(ext)s")),
                "quiet": app_settings.suppress_download_logs,
            }

            try:
                with YoutubeDL(ydl_opts) as ydl:
                    info = ydl.extract_info(media_url, download=True)
                    filename = ydl.prepare_filename(info)
                    logger.info(f"Saved to: {filename}")
            except DownloadError:
                logger.warning(f"Failed to download media from {media_url}")
                return None

            media = MediaAttachment(ContentType.VIDEO, path=filename)

        return media

    @staticmethod
    async def __prepare_payload(data: dict[str, Any]) -> dict[str, Any]:
        """
        Clean and optionally translate APOD data fields.

        Args:
            data (dict[str, Any]): Raw JSON response from NASA API.

        Returns:
            dict[str, Any]: Cleaned and enriched APOD data.
        """
        data.pop("copyright", None)
        data.pop("service_version", None)

        if app_settings.enable_translation:
            translated_texts = (await HttpClient.translate(texts=[data["title"], data["explanation"]]))["translations"]

            data["title_ru"] = translated_texts[0]["text"]
            data["explanation_ru"] = translated_texts[1]["text"]

        return data

    async def __get_apod_data(self, apod_date: str | None, is_random: bool) -> dict[str, Any]:
        """
        Fetch APOD JSON data and prepare it for database insertion.

        Args:
            apod_date (str | None): Specific date to fetch, or None.
            is_random (bool): Whether to request a random APOD.

        Returns:
            dict[str, Any]: Final prepared data with optional translation.
        """
        apod_json: dict[str, Any] = await HttpClient.get(url=self.__get_apod_url(apod_date, is_random))

        if isinstance(apod_json, list):
            apod_json = apod_json[0]

        return await self.__prepare_payload(apod_json)

    @staticmethod
    async def __send_chat_action(dialog_manager: DialogManager, media_type: str) -> None:
        """
        Send a chat action (e.g., 'uploading photo/video') based on the APOD media type.

        Improves UX by showing a loading indicator while media is being prepared.

        Args:
            dialog_manager (DialogManager): Dialog context, used to access bot and chat ID.
            media_type (str): Media type string ("image" or "video").
        """
        bot: Bot | None = dialog_manager.event.bot

        if bot:
            event: Message | CallbackQuery = cast(Message | CallbackQuery, dialog_manager.event)

            if isinstance(event, Message):
                chat_id: int = event.chat.id
            elif isinstance(event, CallbackQuery):
                message = cast(Message, event.message)
                chat_id = message.chat.id
            else:
                raise ValueError(f"Event is not a Message or CallbackQuery ({type(event)}).")

            if media_type == "image":
                await bot.send_chat_action(chat_id, ChatAction.UPLOAD_PHOTO)
            elif media_type == "video":
                await bot.send_chat_action(chat_id, ChatAction.UPLOAD_VIDEO)

    async def __call__(
        self, dialog_manager: DialogManager, i18n: TranslatorRunner, language_code: str, bot: Bot, **_: Any
    ) -> dict[str, Any]:
        """
        Callable interface to prepare dialog context with APOD content.

        Args:
            dialog_manager (DialogManager): Dialog state/context manager.
            i18n (TranslatorRunner): Translation runner.
            language_code (str): Current user language.
            **_ (unused): Ignored extra arguments.

        Returns:
            dict[str, Any]: Dialog context data with localized UI strings and APOD media if available.
        """
        apod_date = dialog_manager.dialog_data.pop("apod_date", None)
        is_random = dialog_manager.dialog_data.pop("is_random", False)

        if not apod_date and not is_random:
            apod_date = datetime.today().strftime("%Y-%m-%d")

        apod: ApodProtocol | None = cast(ApodProtocol | None, await self.__apod_crud.get(date=apod_date))

        if apod:
            if not apod.file_id:
                media: MediaAttachment | None = None
            else:
                media = MediaAttachment(
                    ApodContentType.get_aiogram_type(apod.media_type), file_id=MediaId(file_id=apod.file_id)
                )
        else:
            apod_data: dict[str, Any] = await self.__get_apod_data(apod_date=apod_date, is_random=is_random)
            apod = cast(ApodProtocol, await self.__apod_crud.get_or_create(**apod_data))
            media = await self.__get_apod_media(apod.media_type, apod.url, apod.date.strftime("%Y-%m-%d"))

        if not apod.file_id:
            await self.__send_chat_action(dialog_manager, apod.media_type)

        result = {
            "select_date_button_text": i18n.get("select_date"),
            "random_picture_button_text": i18n.get("random_picture"),
            "explanation_button_text": i18n.get("explanation"),
            "main_menu_button_text": i18n.get("main_menu"),
        }

        if media:
            result |= {
                "apod_caption": i18n.get(
                    "apod_caption",
                    date=apod.date.strftime("%Y-%m-%d"),
                    title=apod.title_ru if language_code == "ru" else apod.title,
                ),
                "resources": media,
                "apod_id": apod.id,
                "language_code": language_code,
            }

            return result

        result |= {"media_not_exist_message": i18n.get("media_not_exist")}
        return result
