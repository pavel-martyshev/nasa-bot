from tortoise.contrib.pydantic import PydanticModel
from tortoise.transactions import atomic

from database.postgres.models.APOD import APOD
from database.postgres.schemas.schemas import get_model, Schema


class APODCRUD:
    @staticmethod
    @atomic()
    async def get_apod(**kwargs) -> PydanticModel | None:
        apod: APOD | None = await APOD.get_or_none(**kwargs)

        if apod:
            return await get_model(Schema.APODSchema, apod)

        return None

    @staticmethod
    @atomic()
    async def get_or_create(**kwargs) -> PydanticModel:
        apod: APOD | None = await APOD.get_or_none(date=kwargs.get("date"))

        return await get_model(Schema.APODSchema, apod if apod else await APOD.create(**kwargs))
