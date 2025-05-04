import time

from tortoise import Model
from tortoise.fields import IntField, BigIntField, BooleanField


class BaseModel(Model):
    id = IntField(primary_key=True)
    created_at = BigIntField(default=lambda: int(time.time()))
    is_deleted = BooleanField(default=False)

    class Meta:
        abstract = True
