from enum import Enum

from aiogram.enums import ContentType


class ApodContentType(Enum):
    """
    Enumeration of APOD media types supported by NASA API.

    Values:
        IMAGE: Static image (e.g., JPG, PNG).
        VIDEO: Video content (e.g., YouTube, MP4).
    """
    IMAGE = "image"
    VIDEO = "video"

    @classmethod
    def get_aiogram_type(cls, apod_type: str) -> ContentType:
        """
        Map APOD media type string to corresponding aiogram ContentType.

        Args:
            apod_type (str): Media type string from NASA API.

        Returns:
            ContentType: Corresponding aiogram content type (PHOTO, VIDEO, or UNKNOWN).
        """
        match apod_type:
            case cls.IMAGE.value:
                return ContentType.PHOTO
            case cls.VIDEO.value:
                return ContentType.VIDEO
            case _:
                return ContentType.UNKNOWN
