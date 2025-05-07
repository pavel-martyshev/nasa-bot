from typing import Dict, Union, Any, List

from aiohttp import ClientResponse

from config import app_settings
from utils.http_client.request_executor import request_executor


class HttpClient:
    @staticmethod
    @request_executor()
    async def get(response: ClientResponse, **_) -> Dict[str, Any]:
        return await response.json()

    @staticmethod
    @request_executor(method="POST")
    async def __execute_translation(response: ClientResponse, **_) -> Dict[str, Any]:
        return await response.json()

    @staticmethod
    async def __prepare_translate_request(texts: str | List[str]) -> Dict[str, Union[str, Dict[str, str]]]:
        return {
            "url": app_settings.api.translate_api_url,
            "headers":{
                "Content-Type": "application/json",
                "Authorization": f"Api-Key {app_settings.api.translate_api_key}"
            },
            "json":{
                "folderId": app_settings.api.folder_id,
                "texts": texts if isinstance(texts, list) else [texts],
                "targetLanguageCode": "ru",
                "sourceLanguageCode": "en"
            }
        }

    @classmethod
    async def translate(cls, *, texts: str | List[str]) -> Dict[str, Any]:
        return await cls.__execute_translation(**(await cls.__prepare_translate_request(texts)))
