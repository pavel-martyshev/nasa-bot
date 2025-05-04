from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import MODEL
from tortoise.transactions import atomic

from utils.enums.Schema import Schema


class BaseCrud:
    @staticmethod
    async def _get_model_schema(schema: Schema, db_model: MODEL) -> PydanticModel | None:
        if db_model is None:
            return None

        return await schema.value.from_tortoise_orm(db_model)

    @atomic()
    async def get(self, **kwargs) -> PydanticModel | None:
        pass

    @atomic()
    async def get_or_create(self, **kwargs) -> PydanticModel | None:
        pass

    @atomic()
    async def update(self, db_id: int, **kwargs):
        pass
