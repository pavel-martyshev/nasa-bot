from collections import namedtuple
from collections.abc import AsyncGenerator
from datetime import date, datetime
from typing import Any
from unittest.mock import AsyncMock, patch

import pytest
from aiogram_dialog.api.entities import MediaAttachment
from fluentogram import TranslatorHub
from yarl import URL

from config import app_settings
from database.postgres.models.apod import APODModel
from dialogs.apod.getters.apod_menu import ApodProvider
from tests.utils.factories.dialog_manager_factory import DialogManagerFactory

TEXTS = namedtuple(
    "TEXTS",
    [
        "explanation_button_text",
        "main_menu_button_text",
        "random_picture_button_text",
        "select_date_button_text"
    ]
)


class TestMenu:
    _texts_to_language_code: dict[str, TEXTS] = {
        "ru": TEXTS(
            "Описание 💭",
            "Главное меню",
            "Случайная картинка 👀",
            "Выбрать дату 📅"
        ),
        "en": TEXTS(
            "Explanation 💭",
            "Main menu",
            "Random picture 👀",
            "Select date 📅"
        )
    }

    async def _test_available_video_or_image(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub,
            get_return_value: dict[str, str],
            translate_return_value: dict[str, list[dict[str, str]]],
            language_code: str,
            dialog_data: dict[str, Any],
            apod_caption: str
    ) -> None:
        mock_get.return_value = get_return_value
        mock_translate.return_value = translate_return_value

        dialog_manager_factory = DialogManagerFactory(dialog_data)

        result = await ApodProvider()(
            dialog_manager_factory.dialog_manager,
            i18n=translator_hub.get_translator_by_locale(language_code),
            language_code=language_code
        )
        texts = self._texts_to_language_code[language_code]

        assert result["apod_caption"] == apod_caption
        assert result["apod_id"] == 1
        assert result["explanation_button_text"] == texts.explanation_button_text
        assert result["language_code"] == language_code
        assert result["main_menu_button_text"] == texts.main_menu_button_text
        assert result["random_picture_button_text"] == texts.random_picture_button_text
        assert isinstance(result["resources"], MediaAttachment)
        assert result["select_date_button_text"] == texts.select_date_button_text

    async def _test_unavailable_video(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub,
            get_return_value: dict[str, str],
            translate_return_value: dict[str, list[dict[str, str]]],
            language_code: str,
            dialog_data: dict[str, Any],
            media_not_exist_message: str
    ) -> None:
        mock_get.return_value = get_return_value
        mock_translate.return_value = translate_return_value

        dialog_manager_factory = DialogManagerFactory(dialog_data)

        result = await ApodProvider()(
            dialog_manager_factory.dialog_manager,
            i18n=translator_hub.get_translator_by_locale(language_code),
            language_code=language_code
        )
        texts = self._texts_to_language_code[language_code]

        assert result["media_not_exist_message"] == media_not_exist_message
        assert result["main_menu_button_text"] == texts.main_menu_button_text
        assert result["random_picture_button_text"] == texts.random_picture_button_text
        assert result["select_date_button_text"] == texts.select_date_button_text

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_image_ru(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        await self._test_available_video_or_image(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": "2025-05-05",
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "image",
                "url": "https://api.nasa.gov/fake.jpg"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "ru",
            {
                "apod_date": "2025-05-05",
                "is_random": False
            },
            "Дата: *\u20682025-05-05\u2069*\n\n\u2068Тестовый заголовок\u2069"
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_today_image_ru(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        today: str = datetime.today().strftime("%Y-%m-%d")

        await self._test_available_video_or_image(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": today,
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "image",
                "url": "https://api.nasa.gov/fake.jpg"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "ru",
            {},
            f"Дата: *\u2068{today}\u2069*\n\n\u2068Тестовый заголовок\u2069"
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_available_video_ru(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        await self._test_available_video_or_image(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": "2025-05-06",
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "video",
                "url": "https://www.youtube.com/embed/rQcKIN9vj3U?rel=0"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "ru",
            {
                "apod_date": "2025-05-06",
                "is_random": False
            },
            "Дата: *\u20682025-05-06\u2069*\n\n\u2068Тестовый заголовок\u2069"
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_unavailable_video_ru(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        await self._test_unavailable_video(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": "2013-02-18",
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "video",
                "url": "https://www.youtube.com/embed/90Omh7_I8vI?rel=0"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "ru",
            {
                "apod_date": "2013-02-18",
                "is_random": False
            },
            ("😞 К сожалению, данные за выбранную дату сейчас недоступны.\n\n"
             "Возможно, изображение было удалено или размещено на внешнем ресурсе. "
             "Попробуйте выбрать другую дату.")
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_image_en(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        await self._test_available_video_or_image(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": "2025-05-05",
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "image",
                "url": "https://api.nasa.gov/fake.jpg"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "en",
            {
                "apod_date": "2025-05-05",
                "is_random": False
            },
            "Date: *\u20682025-05-05\u2069*\n\n\u2068Test title\u2069"
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_today_image_en(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        today: str = datetime.today().strftime("%Y-%m-%d")

        await self._test_available_video_or_image(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": today,
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "image",
                "url": "https://api.nasa.gov/fake.jpg"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "en",
            {},
            f"Date: *\u2068{today}\u2069*\n\n\u2068Test title\u2069"
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_available_video_en(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        await self._test_available_video_or_image(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": "2025-05-06",
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "video",
                "url": "https://www.youtube.com/embed/rQcKIN9vj3U?rel=0"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "en",
            {
                "apod_date": "2025-05-06",
                "is_random": False
            },
            "Date: *\u20682025-05-06\u2069*\n\n\u2068Test title\u2069"
        )

    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    @pytest.mark.asyncio
    async def test_apod_provider_with_unavailable_video_en(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            translator_hub: TranslatorHub
    ) -> None:
        await self._test_unavailable_video(
            mock_get,
            mock_translate,
            translator_hub,
            {
                "date": "2013-02-18",
                "title": "Test title",
                "explanation": "Test explanation",
                "media_type": "video",
                "url": "https://www.youtube.com/embed/90Omh7_I8vI?rel=0"
            },
            {
                "translations": [
                    {"text": "Тестовый заголовок"},
                    {"text": "Тестовое пояснение"}
                ]
            },
            "en",
            {
                "apod_date": "2013-02-18",
                "is_random": False
            },
            ("😞 Unfortunately, the data for this date is currently unavailable.\n"
             "The image may have been removed or hosted externally. Please try selecting a different date.")
        )

    @pytest.mark.asyncio
    @patch("dialogs.apod.getters.apod_menu.HttpClient.translate")
    @patch("dialogs.apod.getters.apod_menu.HttpClient.get")
    async def test_apod_provider_creates_apod_record(
            self,
            mock_get: AsyncMock,
            mock_translate: AsyncMock,
            init_db: AsyncGenerator[None, Any],
            translator_hub: TranslatorHub
    ) -> None:
        mock_get.return_value = {
            "date": "2025-05-05",
            "title": "Test title",
            "explanation": "Test explanation",
            "media_type": "image",
            "url": "https://api.nasa.gov/fake.jpg",
            "hdurl": "https://api.nasa.gov/fake_hd.jpg"
        }

        mock_translate.return_value = {
            "translations": [
                {"text": "Тестовый заголовок"},
                {"text": "Тестовое пояснение"}
            ]
        }

        dialog_manager_factory = DialogManagerFactory({"apod_date": "2025-05-05", "is_random": False})
        middleware_data = {
            "i18n": translator_hub.get_translator_by_locale("en"),
            "language_code": "en"
        }

        await ApodProvider()(dialog_manager_factory.dialog_manager, **middleware_data)
        apod = await APODModel.get_or_none(date="2025-05-05")

        assert apod is not None
        assert apod.title == "Test title"
        assert apod.title_ru == "Тестовый заголовок"
        assert apod.date == date(2025, 5, 5)
        assert apod.explanation == "Test explanation"
        assert apod.explanation_ru == "Тестовое пояснение"
        assert apod.url == "https://api.nasa.gov/fake.jpg"
        assert apod.hdurl == "https://api.nasa.gov/fake_hd.jpg"
        assert apod.media_type == "image"
        assert apod.file_id is None

        await ApodProvider()(dialog_manager_factory.dialog_manager, **middleware_data)

        assert await APODModel.all().count() == 1

        apod = await APODModel.get_or_none(date="2025-05-05")
        apod.file_id = "abc123"
        await apod.save()

        result = await ApodProvider()(dialog_manager_factory.dialog_manager, **middleware_data)

        assert result["resources"].file_id.file_id == "abc123"

    @pytest.mark.asyncio
    async def test_get_apod_url(self) -> None:
        url_parts = ApodProvider._ApodProvider__apod_url_parts  # type: ignore[attr-defined]
        url = ApodProvider._ApodProvider__get_apod_url(ApodProvider(), "2025-05-05", False)  # type: ignore[attr-defined]

        expected_url = URL(
            f"https://api.nasa.gov/{url_parts[0]}/{url_parts[1]}?api_key={app_settings.api.nasa_api_key}&date=2025-05-05"
        )
        assert url == expected_url

        url = ApodProvider._ApodProvider__get_apod_url(ApodProvider(), None, True)  # type: ignore[attr-defined]

        expected_url = URL(
            f"https://api.nasa.gov/{url_parts[0]}/{url_parts[1]}?api_key={app_settings.api.nasa_api_key}&count=1"
        )
        assert url == expected_url

        url = ApodProvider._ApodProvider__get_apod_url(ApodProvider(), "2024-06-26", True)  # type: ignore[attr-defined]

        expected_url = URL(
            f"https://api.nasa.gov/{url_parts[0]}/{url_parts[1]}?api_key={app_settings.api.nasa_api_key}&date=2024-06-26"
        )
        assert url == expected_url
