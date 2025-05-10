from datetime import datetime
from typing import Protocol


class BaseProtocol(Protocol):
    id: int
    created_at: int
    is_deleted: bool


class APODProtocol(BaseProtocol):
    title: str
    title_ru: str
    date: datetime
    explanation: str
    explanation_ru: str
    url: str
    hdurl: str
    media_type: str
    file_id: str
