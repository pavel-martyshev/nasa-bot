from enum import Enum

from aiogram.enums import ContentType


class APODContentType(Enum):
    IMAGE = "image"
    VIDEO = "video"

    @classmethod
    def get_aiogram_type(cls, apod_type: str) -> ContentType:
        match apod_type:
            case cls.IMAGE.value:
                return ContentType.PHOTO
            case cls.VIDEO.value:
                return ContentType.VIDEO
            case _:
                return ContentType.UNKNOWN
