from datetime import datetime
from typing import Any, cast

from aiogram import Bot
from aiogram.enums import ContentType
from aiogram.types import User
from aiogram_dialog import DialogManager
from aiogram_dialog.api.entities import MediaAttachment, MediaId
from aiohttp import ClientResponse
from fluentogram import TranslatorRunner
from yarl import URL
from yt_dlp import DownloadError

from config import app_settings
from config.log_config import log_return_value, logger
from database.postgres.core.CRUD.apod import ApodCrud
from database.postgres.core.protocols import ApodProtocol
from dialogs.apod.service.apod_other_media_resolver import ApodOtherMediaResolver
from dialogs.apod.service.chat_action_sender import ChatActionSender
from dialogs.apod.service.video_downloader import VideoDownloader
from utils.enums.apod_content_type import ApodContentType
from utils.http_client import HttpClient


class ApodProvider:
    """
    Fetches and prepares NASA APOD data for dialog rendering.

    Handles media download, translation, and caption formatting.
    """

    __apod_url_parts: tuple[str, str] = "planetary", "apod"
    __apod_crud: ApodCrud = ApodCrud()
    __other_media_resolver: ApodOtherMediaResolver = ApodOtherMediaResolver()
    __chat_action_sender: ChatActionSender | None = None

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

    async def __get_apod_media(self, media_type: str, media_url: str, apod_date: str) -> MediaAttachment:
        """
        Download APOD media and wrap it as a MediaAttachment.

        Args:
            media_type (str): Type of media ("image", "video" or "other").
            media_url (str): URL to the media resource.
            apod_date (str): Date of the APOD (used for logging).

        Returns:
            MediaAttachment: Wrapped media.
        """
        logger.info(f"APOD url at {apod_date}: {media_url}")

        if media_type == "other" and self.__other_media_resolver.src and self.__other_media_resolver.media_type:
            media_url = str(app_settings.api.nasa_apod_base_url / self.__other_media_resolver.src)
            media_type = self.__other_media_resolver.media_type

        if self.__chat_action_sender:
            await self.__chat_action_sender.send_chat_action(cast(str, media_type))

        if media_type == "image":
            return MediaAttachment(ContentType.PHOTO, media_url)

        try:
            VideoDownloader.download(media_url)
        except DownloadError:
            logger.warning(f"Failed to download media from {media_url}")
            raise

        return MediaAttachment(ContentType.VIDEO, path=VideoDownloader.filename, supports_streaming=True)

    async def __prepare_payload(self, data: dict[str, Any]) -> dict[str, Any]:
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

            if data["media_type"] == "other":
                await self.__other_media_resolver(data["date"])

                if self.__other_media_resolver.src and self.__other_media_resolver.media_type:
                    data["url"] = str(URL(app_settings.api.nasa_apod_base_url / self.__other_media_resolver.src))
                    data["media_type"] = self.__other_media_resolver.media_type

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
        response: ClientResponse = await HttpClient.get(url=self.__get_apod_url(apod_date, is_random))
        apod_json: dict[str, Any] = await response.json()

        if isinstance(apod_json, list):
            apod_json = apod_json[0]

        return await self.__prepare_payload(apod_json)

    async def __call__(
        self,
        dialog_manager: DialogManager,
        i18n: TranslatorRunner,
        language_code: str,
        bot: Bot,
        event_from_user: User,
        **_: Any,
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
        self.__chat_action_sender = ChatActionSender(event_from_user.id, bot)

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

            try:
                media = await self.__get_apod_media(apod.media_type, apod.url, apod.date.strftime("%Y-%m-%d"))
            except DownloadError:
                media = None

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
