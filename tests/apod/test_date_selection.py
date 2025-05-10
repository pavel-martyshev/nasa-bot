from datetime import datetime
from typing import Optional

import pytest
from fluentogram import TranslatorHub

from dialogs.apod.getters.apod_date_selection import getter
from tests.utils.factories.dialog_manager_factory import DialogManagerFactory


class TestDateSelection:
    _date_request_ru = ("Введите дату в формате ДД.ММ.ГГГГ\n"
                        "Минимальная дата `16.06.1995`\n"
                        "Максимальная дата `\u2068{today}\u2069`")

    _date_request_en = ("Enter date in MM/DD/YYYY format\n"
                        "Minimum date `06/16/1995`\n"
                        "Maximum date `\u2068{today}\u2069`")

    @staticmethod
    async def _test_getter(
            translator_hub: TranslatorHub,
            dialog_data: dict[str, bool],
            language_code: str,
            back_button_text: str,
            date_request: str,
            *,
            incorrect_date_message: Optional[str] = None,
            incorrect_format_message: Optional[str] = None,
    ) -> None:
        dialog_manager_factory = DialogManagerFactory(dialog_data)

        result = await getter(
            dialog_manager_factory.dialog_manager,
            i18n=translator_hub.get_translator_by_locale(language_code),
            language_code=language_code,
        )

        assert result["back_button_text"] == back_button_text
        assert result["date_request"] == date_request

        if incorrect_date_message:
            assert result["incorrect_date_message"] == incorrect_date_message

        if incorrect_format_message:
            assert result["incorrect_format_message"] == incorrect_format_message

    @pytest.mark.asyncio
    async def test_getter_with_current_date_ru(self, translator_hub: TranslatorHub) -> None:
        today = datetime.today().strftime("%d.%m.%Y")

        await self._test_getter(
            translator_hub,
            {},
            "ru",
            "Назад",
            self._date_request_ru.format(today=today),
        )

    @pytest.mark.asyncio
    async def test_getter_with_incorrect_date_ru(self, translator_hub: TranslatorHub) -> None:
        today = datetime.today().strftime("%d.%m.%Y")

        await self._test_getter(
            translator_hub,
            {"incorrect_date": True},
            "ru",
            "Назад",
            self._date_request_ru.format(today=today),
            incorrect_date_message="⚠️ Некорректная дата"
        )

    @pytest.mark.asyncio
    async def test_getter_with_incorrect_format_ru(self, translator_hub: TranslatorHub) -> None:
        today = datetime.today().strftime("%d.%m.%Y")

        await self._test_getter(
            translator_hub,
            {"incorrect_format": True},
            "ru",
            "Назад",
            self._date_request_ru.format(today=today),
            incorrect_format_message="⚠️ Некорректный формат"
        )

    @pytest.mark.asyncio
    async def test_getter_with_current_date_en(self, translator_hub: TranslatorHub) -> None:
        today = datetime.today().strftime("%m/%d/%Y")

        await self._test_getter(
            translator_hub,
            {},
            "en",
            "Back",
            self._date_request_en.format(today=today)
        )

    @pytest.mark.asyncio
    async def test_getter_with_incorrect_date_en(self, translator_hub: TranslatorHub) -> None:
        today = datetime.today().strftime("%m/%d/%Y")

        await self._test_getter(
            translator_hub,
            {"incorrect_date": True},
            "en",
            "Back",
            self._date_request_en.format(today=today),
            incorrect_date_message="⚠️ Incorrect date"
        )

    @pytest.mark.asyncio
    async def test_getter_with_incorrect_format_en(self, translator_hub: TranslatorHub) -> None:
        today = datetime.today().strftime("%m/%d/%Y")

        await self._test_getter(
            translator_hub,
            {"incorrect_format": True},
            "en",
            "Back",
            self._date_request_en.format(today=today),
            incorrect_format_message="⚠️ Incorrect format"
        )
