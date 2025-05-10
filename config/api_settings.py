from dataclasses import dataclass
from typing import Any

from yarl import URL


@dataclass
class APISettings:
    """
    Settings for all API configurations.

    Attributes:
        nasa_api_base_url: Base URL of the NASA API.
        nasa_api_key: API key for authentication.
        translate_api_key: API key for translation.
        folder_id: Yandex cloud folder ID.
    """
    nasa_api_base_url: URL
    nasa_api_key: str

    translate_api_url: URL
    translate_api_key: str
    folder_id: str

    bot_api_host: str
    bot_api_port: int

    def __post_init__(self) -> None:
        error_message = "{argument_name} must be set"

        if not self.nasa_api_base_url:
            raise KeyError(error_message.format(argument_name="nasa_api_base_url"))

        if not self.nasa_api_key:
            raise KeyError(error_message.format(argument_name="nasa_api_key"))

        if not self.translate_api_url:
            raise KeyError(error_message.format(argument_name="translate_api_url"))

        if not self.translate_api_key:
            raise KeyError(error_message.format(argument_name="translate_api_key"))

        if not self.folder_id:
            raise KeyError(error_message.format(argument_name="folder_id"))

    def build_url(self, *args: str, **kwargs: Any) -> URL:
        """
        Build a full API URL by joining base URL with additional path parts and optional query parameters.

        Args:
            *args: Parts of the URL path to append.
            **kwargs: Query parameters to add to the URL.

        Returns:
            Full URL ready to use for an API request.
        """
        full_url = self.nasa_api_base_url

        if args:
            full_url = full_url.joinpath(*args)

        if kwargs:
            full_url = full_url.with_query(**kwargs)

        return full_url
