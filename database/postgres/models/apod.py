from tortoise.fields import CharField, DateField, TextField

from database.postgres.core.base_model import OrmBaseModel


class ApodModel(OrmBaseModel):
    """
    Tortoise ORM model for NASA's Astronomy Picture of the Day (APOD).

    Fields:
        title (str): Original APOD title.
        title_ru (str | None): Translated title.
        date (date): Date of the APOD.
        explanation (str): Original APOD description.
        explanation_ru (str | None): Translated description.
        url (str): Media URL.
        hdurl (str | None): High-definition media URL.
        media_type (str): Type of media (e.g., "image", "video").
        file_id (str | None): Telegram file identifier.

    Meta:
        table (str): Name of the database table.
        ordering (list[str]): Default ordering by ID.
    """

    title = CharField(max_length=100, null=False)
    title_ru = CharField(max_length=100, null=True)

    date = DateField(null=False)

    explanation = TextField(null=False)
    explanation_ru = TextField(null=True)

    url = CharField(max_length=150, null=False)
    hdurl = CharField(max_length=150, null=True)

    media_type = CharField(max_length=15, null=False)
    file_id = CharField(max_length=150, null=True)

    class Meta:
        table = "apod"
        ordering = ["id"]
