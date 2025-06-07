from dataclasses import dataclass
from typing import Any

from yarl import URL


@dataclass
class APISettings:
    """
    Stores configuration for NASA, translation, and webhook-related settings.

    Attributes:
    nasa_api_base_url (URL): Base URL for the NASA API.
    nasa_api_key (str): API key for NASA API.
    translate_api_url (URL): Base URL for the translation API.
    translate_api_key (str): API key for the translation API.
    folder_id (str): Yandex Cloud folder ID.
    base_webhook_url (URL | None): Base URL used for Telegram webhook.
    webhook_host (str | None): Host on which the webhook server runs.
    webhook_port (int): Port used for the webhook server.
    webhook_path (str | None): Path that handles incoming Telegram updates.
    webhook_key (str | None): Secret token used to validate webhook requests.
    """

    nasa_api_base_url: URL
    nasa_api_key: str

    translate_api_url: URL
    translate_api_key: str
    folder_id: str

    base_webhook_url: URL
    webhook_host: str | None
    webhook_port: int
    webhook_path: str | None
    webhook_key: str | None

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

    @property
    def is_webhook_enabled(self) -> bool:
        """
        True if all webhook-related settings are defined.
        """
        if self.base_webhook_url and self.webhook_host and self.webhook_port and self.webhook_path:
            return True

        return False

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

    def get_full_webhook_url(self) -> URL:
        """
        Return full webhook URL by combining base URL and path.

        Raises:
            ValueError: if webhook_host or webhook_path is not set.
        """
        if not (self.webhook_host and self.webhook_path):
            raise ValueError("Cannot build webhook URL: both webhook_host and webhook_port must be set")

        return self.base_webhook_url.joinpath(self.webhook_path)
