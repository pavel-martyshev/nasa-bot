from tortoise.fields import BigIntField, CharField, IntField

from database.postgres.core.base_model import OrmBaseModel


class UserModel(OrmBaseModel):
    """
    Tortoise ORM model representing a Telegram user.

    Fields:
        telegram_id (int): Unique Telegram user ID.
        username (str | None): Telegram username.
        first_name (str | None): User's first name.
        last_name (str | None): User's last name.
        language_code (str): Language code (e.g., "en", "ru").
        last_activity_time (int): Unix timestamp of the user's last activity.

    Meta:
        table (str): Name of the database table.
        ordering (list[str]): Default ordering by ID.
    """
    telegram_id = IntField(null=False)
    username = CharField(max_length=100, null=True)

    first_name = CharField(max_length=100, null=True)
    last_name = CharField(max_length=100, null=True)

    language_code = CharField(max_length=5, null=False)
    last_activity_time = BigIntField(null=False)

    class Meta:
        table = "users"
        ordering = ["id"]
