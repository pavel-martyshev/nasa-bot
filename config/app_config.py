import os
from dataclasses import dataclass
from pathlib import Path

from dotenv import load_dotenv
from yarl import URL

from config.api_settings import APISettings
from config.database_settings import DatabaseSettings
from config.logs_settings import LogsSettings

SOURCE_PATH = Path(__file__).parent.parent

# Load environment variables from .env or fallback to .env.example
if os.path.exists(Path.joinpath(SOURCE_PATH, ".env")):
    load_dotenv(Path.joinpath(SOURCE_PATH, ".env"))
else:
    load_dotenv(Path.joinpath(SOURCE_PATH, ".env.example"))


@dataclass
class AppSettings:
    """
    Main application settings container.

    Attributes:
        token (str): Telegram bot token.
        resources_path (str): Path to static resources.
        temp_resources_path (str): Path to temporary resources.
        suppress_download_logs (bool): Suppress downloader logs if True.
        web_app_url (str): Public URL of the deployed WebApp.
        enable_translation (bool): Whether translation features are enabled.

        logs (LogsSettings): Logging configuration.
        db (DatabaseSettings): Database connection settings.
        api (APISettings): External API configuration.
    """

    token: str
    resources_path: str
    temp_resources_path: str
    suppress_download_logs: bool
    web_app_url: str
    enable_translation: bool

    logs: LogsSettings
    db: DatabaseSettings
    api: APISettings

    def __post_init__(self) -> None:
        if not self.token:
            raise ValueError("Token is required")

        if not self.resources_path:
            raise ValueError("Resources path is required")

        if not self.temp_resources_path:
            raise ValueError("Temporary resources path is required")

    @staticmethod
    def get_date_format(language_code: str) -> str:
        """
        Return date format string based on language code.

        Args:
            language_code (str): Language code, e.g., "ru" or "en".

        Returns:
            str: Corresponding date format string.
        """
        match language_code:
            case "ru":
                return "%d.%m.%Y"
            case _:
                return "%m/%d/%Y"

    def get_full_temp_path(self) -> Path:
        """
        Get the full path to the temporary resources directory.

        Returns:
            Path: Combined path of resources and temporary folder.

        Raises:
            KeyError: If either path is missing.
        """
        if not (self.resources_path and self.temp_resources_path):
            raise KeyError("Resources path or temporary resources path is missing.")

        return Path(self.resources_path, self.temp_resources_path)


def load_settings() -> AppSettings:
    """
    Load settings from environment variables and return an AppSettings instance.

    Returns:
        AppSettings: Configured application settings.
    """
    webhook_port: str = os.getenv("WEBHOOK_PORT") or "8000"

    return AppSettings(
        token=os.getenv("TOKEN", ""),
        resources_path=os.getenv("RESOURCES_PATH", ""),
        temp_resources_path=os.getenv("TEMP_RESOURCES_PATH", ""),
        suppress_download_logs=bool(os.getenv("SUPPRESS_DOWNLOAD_LOGS")),
        web_app_url=os.getenv("WEB_APP_URL", ""),
        enable_translation=bool(os.getenv("ENABLE_TRANSLATION")),
        logs=LogsSettings(
            level=os.getenv("LEVEL", "INFO"),
            dir_name=os.getenv("DIR_NAME", "logs"),
            file_name=os.getenv("FILE_NAME", "logs.log"),
            handlers_format=os.getenv("HANDLERS_FORMAT", "%(asctime)s | %(levelname)s | %(message)s"),
            date_format=os.getenv("DATE_FORMAT", "%Y-%m-%d"),
            time_rotating=os.getenv("TIME_ROTATING", "D"),
            backup_count=int(os.getenv("BACKUP_COUNT", 10)),
        ),
        db=DatabaseSettings(
            redis_host=os.getenv("REDIS_HOST", "localhost"),
            redis_port=int(os.getenv("REDIS_PORT", 6379)),
            redis_db_number=int(os.getenv("REDIS_DB_NUMBER", 0)),
            postgres_host=os.getenv("POSTGRES_HOST", "localhost"),
            postgres_port=int(os.getenv("POSTGRES_PORT", 5432)),
            postgres_user=os.getenv("POSTGRES_USER", "postgres"),
            postgres_password=os.getenv("POSTGRES_PASSWORD", "<PASSWORD>"),
            postgres_db_name=os.getenv("POSTGRES_DB_NAME", "postgres"),
        ),
        api=APISettings(
            nasa_api_base_url=URL(os.getenv("NASA_API_BASE_URL", "")),
            nasa_api_key=os.getenv("NASA_API_KEY", ""),
            translate_api_url=URL(os.getenv("TRANSLATE_API_URL", "")),
            translate_api_key=os.getenv("TRANSLATE_API_KEY", ""),
            folder_id=os.getenv("FOLDER_ID", ""),
            base_webhook_url=URL(os.getenv("BASE_WEBHOOK_URL", "")),
            webhook_host=os.getenv("WEBHOOK_HOST"),
            webhook_port=int(webhook_port),
            webhook_path=os.getenv("WEBHOOK_PATH"),
            webhook_key=os.getenv("WEBHOOK_KEY"),
        ),
    )


# Create the final application settings instance
app_settings: AppSettings = load_settings()
