import os
from dataclasses import dataclass

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
        logs: Logging configuration settings.
        api: API configuration settings.
    """
    token: str

    logs: LogsSettings
    db: DatabaseSettings
    api: APISettings

    language_code: str = None

    @property
    def date_format(self) -> str:
        return "%Y-%m-%d" if self.language_code == "en" else "%d.%m.%Y"


def load_settings() -> AppSettings:
    """
    Load settings from environment variables and return an AppSettings instance.

    Returns:
        AppSettings: Configured application settings.
    """
    return AppSettings(
        token=os.getenv("TOKEN"),
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
app_settings = load_settings()
