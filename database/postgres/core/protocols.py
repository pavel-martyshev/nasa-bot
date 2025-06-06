from datetime import datetime
from typing import Protocol


class BaseProtocol(Protocol):
    """
    Base protocol for shared model attributes.

    Attributes:
        id (int): Unique identifier.
        created_at (int): Unix timestamp of creation.
        is_deleted (bool): Soft delete flag.
    """

    id: int
    created_at: int
    is_deleted: bool


class ApodProtocol(BaseProtocol):
    """
    Protocol representing the structure of an APOD model.

    Attributes:
        title (str): Original title.
        title_ru (str): Translated title.
        date (datetime): APOD date.
        explanation (str): Original explanation text.
        explanation_ru (str): Translated explanation text.
        url (str): Media URL.
        hdurl (str): High-definition media URL.
        media_type (str): Type of media (e.g., "image", "video").
        file_id (str): Telegram file identifier.
    """

    title: str
    title_ru: str
    date: datetime
    explanation: str
    explanation_ru: str
    url: str
    hdurl: str
    media_type: str
    file_id: str
