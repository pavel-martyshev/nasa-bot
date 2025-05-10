from tortoise.fields import BigIntField, CharField, IntField

from database.postgres.core.base_model import BaseModel


class UserModel(BaseModel):
    telegram_id = IntField(null=False, blank=False)
    username = CharField(max_length=100, null=True, blank=False)

    first_name = CharField(max_length=100, null=True, blank=False)
    last_name = CharField(max_length=100, null=True, blank=False)

    language_code = CharField(max_length=5, null=False, blank=False)
    last_activity_time = BigIntField(null=False, blank=False)

    class Meta:
        table = "users"
        ordering = ["id"]
