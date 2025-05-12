from dataclasses import dataclass
from typing import Any

from yarl import URL


@dataclass
class APISettings:
    """
    Holds configuration for external APIs and bot server settings.

    Attributes:
        nasa_api_base_url (URL): Base URL for NASA API.
        nasa_api_key (str): NASA API key.
        translate_api_url (URL): Base URL for the translation API.
        translate_api_key (str): Translation API key.
        folder_id (str): Yandex Cloud folder ID.
        bot_api_host (str): Hostname for the bot API server.
        bot_api_port (int): Port for the bot API server.
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

    def build_nasa_url(self, *args: str, **kwargs: Any) -> URL:
        """
        Construct a full NASA API URL from path segments and optional query parameters.

        Args:
            *args: URL path segments to append.
            **kwargs: (optional) Query parameters.

        Returns:
            URL: Fully constructed API URL.
        """
        full_url = self.nasa_api_base_url

        if args:
            full_url = full_url.joinpath(*args)

        if kwargs:
            full_url = full_url.with_query(**kwargs)

        return full_url
