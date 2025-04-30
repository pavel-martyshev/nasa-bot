from dataclasses import dataclass

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

    translate_api_url: str
    translate_api_key: str
    folder_id: str

    bot_api_host: str
    bot_api_port: int

    def build_url(self, *args, **kwargs) -> URL:
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
