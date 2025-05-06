from tortoise.fields import CharField, DateField, TextField

from database.postgres.core.base_model import BaseModel


class APODModel(BaseModel):
    title = CharField(max_length=100, null=False, blank=False)
    title_ru = CharField(max_length=100, null=False, blank=False)

    date = DateField(null=False, blank=False)

    explanation	= TextField(null=False, blank=False)
    explanation_ru = TextField(null=False, blank=False)

    url = CharField(max_length=150, null=False, blank=False)
    hdurl = CharField(max_length=150, null=True, blank=False)

    media_type = CharField(max_length=15, null=False, blank=False)
    file_id = CharField(max_length=150, null=True, blank=False)

    class Meta:
        table = "apod"
        ordering = ["id"]
