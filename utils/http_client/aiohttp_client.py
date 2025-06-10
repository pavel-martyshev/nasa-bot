from typing import Any

from aiohttp import ClientResponse

from config import app_settings
from utils.http_client.request_executor import request_executor


class HttpClient:
    """
    Utility class for making HTTP requests and translating text via external API.
    """

    @staticmethod
    @request_executor()
    async def get(response: ClientResponse, *_: Any, **__: Any) -> Any:
        """
        Perform a GET request and parse the response as JSON.

        Args:
            response (ClientResponse): Response object from aiohttp session.
            *_ (unused): Ignored positional arguments.
            **__ (unused): Ignored keyword arguments.

        Returns:
            Any: Parsed JSON response.
        """
        return await response.json()

    @staticmethod
    @request_executor(method="POST")
    async def __execute_translation(response: ClientResponse, *_: Any, **__: Any) -> Any:
        """
        Perform a POST request to the translation API and return parsed JSON.

        Args:
            response (ClientResponse): Response object from aiohttp session.
            *_ (unused): Ignored positional arguments.
            **__ (unused): Ignored keyword arguments.

        Returns:
            Any: Parsed JSON response.
        """
        return await response.json()

    @staticmethod
    async def __prepare_translate_request(texts: str | list[str]) -> dict[str, Any]:
        """
        Prepare request parameters for the translation API.

        Args:
            texts (str | list[str]): One or more texts to translate.

        Returns:
            dict[str, Any]: Dictionary with URL, headers, and JSON payload.
        """
        return {
            "url": app_settings.api.translate_api_url,
            "headers": {
                "Content-Type": "application/json",
                "Authorization": f"Api-Key {app_settings.api.translate_api_key}",
            },
            "json": {
                "folderId": app_settings.api.folder_id,
                "texts": texts if isinstance(texts, list) else [texts],
                "targetLanguageCode": "ru",
                "sourceLanguageCode": "en",
            },
        }

    @classmethod
    async def translate(cls, *, texts: str | list[str]) -> Any:
        """
        Translate text(s) from English to Russian using external API.

        Args:
            texts (str | list[str]): One or more texts to translate.

        Returns:
            Any: API response with translated texts.
        """
        return await cls.__execute_translation(**(await cls.__prepare_translate_request(texts)))
