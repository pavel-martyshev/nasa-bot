import time

from tortoise import Model
from tortoise.fields import BigIntField, BooleanField, IntField


class OrmBaseModel(Model):
    """
    Abstract base model with common fields.

    Attributes:
        id (int): Primary key.
        created_at (int): Unix timestamp of creation.
        is_deleted (bool): Soft delete flag.
    """
    id = IntField(primary_key=True)
    created_at = BigIntField(default=lambda: int(time.time()))
    is_deleted = BooleanField(default=False)

    class Meta:
        abstract = True
