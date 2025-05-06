import os
from dataclasses import dataclass
from pathlib import Path
from unittest import case

from dotenv import load_dotenv
from yarl import URL

from config.api_settings import APISettings
from config.database_settings import DatabaseSettings
from config.logs_settings import LogsSettings

load_dotenv()


@dataclass
class AppSettings:
    """
    Top-level application settings container.

    Attributes:
        token: Telegram bot token.
        resources_path: Path to static resource files (e.g., images, videos).
        tmp_resources_path: Path to temporary files used during processing.
        quiet_download: If True, suppresses download-related logs or messages (e.g., from youtube-dl).

        logs: Logging configuration settings.
        db: Database configuration settings.
        api: API configuration settings.
    """
    token: str
    resources_path: str
    tmp_resources_path: str
    quiet_download: bool

    logs: LogsSettings
    db: DatabaseSettings
    api: APISettings

    @staticmethod
    def get_date_format(language_code: str) -> str:
        match language_code:
            case "ru":
                return "%d.%m.%Y"
            case _:
                return "%m/%d/%Y"

    def get_full_tmp_path(self) -> Path:
        return Path(self.resources_path, self.tmp_resources_path)


def load_settings() -> AppSettings:
    """
    Load settings from environment variables and return an AppSettings instance.

    Returns:
        AppSettings: Configured application settings.
    """
    return AppSettings(
        token=os.getenv("TOKEN"),
        resources_path=os.getenv("RESOURCES_PATH"),
        tmp_resources_path=os.getenv("TMP_RESOURCES_PATH"),
        quiet_download=bool(os.getenv("QUIET_DOWNLOAD")),

        logs=LogsSettings(
            level=os.getenv("LEVEL"),
            dir_name=os.getenv("DIR_NAME"),
            file_name=os.getenv("FILE_NAME"),
            handlers_format=os.getenv("HANDLERS_FORMAT"),
            date_format=os.getenv("DATE_FORMAT"),
            time_rotating=os.getenv("TIME_ROTATING"),
            backup_count=int(os.getenv("BACKUP_COUNT")),
        ),

        db=DatabaseSettings(
            redis_host=os.getenv("REDIS_HOST"),
            redis_port=int(os.getenv("REDIS_PORT")),
            redis_db_number=int(os.getenv("REDIS_DB_NUMBER")),
            postgres_host=os.getenv("POSTGRES_HOST"),
            postgres_port=int(os.getenv("POSTGRES_PORT")),
            postgres_user=os.getenv("POSTGRES_USER"),
            postgres_password=os.getenv("POSTGRES_PASSWORD"),
            postgres_db_name=os.getenv("POSTGRES_DB_NAME"),
        ),

        api=APISettings(
            nasa_api_base_url=URL(os.getenv("NASA_API_BASE_URL")),
            nasa_api_key=os.getenv("NASA_API_KEY"),
            translate_api_url=os.getenv("TRANSLATE_API_URL"),
            translate_api_key=os.getenv("TRANSLATE_API_KEY"),
            folder_id=os.getenv("FOLDER_ID"),
            bot_api_host=os.getenv("BOT_API_HOST"),
            bot_api_port=int(os.getenv("BOT_API_PORT")),
        )
    )


# Create the final application settings instance
app_settings: AppSettings = load_settings()
