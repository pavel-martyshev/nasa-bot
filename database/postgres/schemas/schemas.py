from enum import Enum

from tortoise.contrib.pydantic import pydantic_model_creator, PydanticModel
from tortoise.models import MODEL

from database.postgres.models.APOD import APOD


class Schema(Enum):
    APODSchema = pydantic_model_creator(APOD)


async def get_model(schema: Schema, db_model: MODEL) -> PydanticModel | None:
    if db_model is None:
        return None

    return await schema.value.from_tortoise_orm(db_model)
