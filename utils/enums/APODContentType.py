from enum import Enum

from aiogram.enums import ContentType


class APODContentType(Enum):
    IMAGE = "image"
    VIDEO = "video"

    @classmethod
    def get_aiogram_type(cls, apod_type: str) -> ContentType | None:
        if apod_type == cls.IMAGE.value:
            return ContentType.PHOTO

        if apod_type == cls.VIDEO.value:
            return ContentType.VIDEO
