from datetime import datetime

class PydanticModel:
    id: int
    created_at: int
    is_deleted: bool

    telegram_id: int
    username: str
    first_name: str
    last_name: str
    language_code: str
    last_activity_time: int

    title: str
    title_ru: str
    date: datetime
    explanation: str
    explanation_ru: str
    url: str
    hdurl: str
    media_type: str
    file_id: str
