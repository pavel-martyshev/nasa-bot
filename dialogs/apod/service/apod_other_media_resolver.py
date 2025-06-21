from typing import cast

from aiohttp import ClientResponse
from bs4 import BeautifulSoup
from bs4.element import AttributeValueList
from yarl import URL

from config import app_settings
from utils.http_client import HttpClient


class ApodOtherMediaResolver:
    """
    Resolves the direct media source and type for "other" type.

    After calling the instance with a date, properties `src` and `media_type`
    will contain the extracted media URL and type (e.g., "video").
    """

    __src: str | AttributeValueList | None = None
    __media_type: str | None = None
    __date: str | None = None

    @property
    def src(self) -> str | None:
        if self.__src:
            return str(self.__src)

        return None

    @property
    def media_type(self) -> str | None:
        return self.__media_type

    async def __set_media_src(self, url: URL) -> None:
        """
        Extract media source and type from the APOD HTML page.

        Args:
            url (URL): URL of the APOD HTML page to parse.

        Raises:
            ValueError: If source or media type could not be extracted.
        """

        response: ClientResponse = await HttpClient.get(str(url))
        bs: BeautifulSoup = BeautifulSoup(await response.text(), "html.parser")
        source = bs.source

        if source:
            src = source.get("src")

            if not src:
                raise ValueError("Failed to get source url")

            self.__src = src
            media_type, _ = cast(str, source.get("type")).rsplit("/")

            if not media_type:
                raise ValueError(f"Failed to get media type ({source.get('type')})")

            self.__media_type = media_type

    async def __call__(self, apod_date: str):
        """
        Entry point for resolving APOD media from a date string.

        Args:
            apod_date (str): Date string in the format "YYYY-MM-DD".

        Side effects:
            Sets the internal `__src` and `__media_type` properties.
        """

        self.__date = apod_date
        full_apod_url = app_settings.api.nasa_apod_base_url / f"ap{apod_date[2:].replace('-', '')}.html"
        await self.__set_media_src(full_apod_url)
