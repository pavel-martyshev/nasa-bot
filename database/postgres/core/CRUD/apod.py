from typing import Any

from tortoise.contrib.pydantic import PydanticModel

from database.postgres.core.CRUD.base_crud import BaseCrud
from database.postgres.models.apod import APODModel
from utils.enums.Schema import Schema


class APODCRUD(BaseCrud):
    @property
    def _model(self) -> type[APODModel]:
        return APODModel

    @property
    def _schema(self) -> Schema:
        return Schema.APODSchema

    async def get_or_create(self, **kwargs: Any) -> PydanticModel | None:
        apod: APODModel | None = await APODModel.get_or_none(date=kwargs.get("date"))
        return await self._get_model_schema(Schema.APODSchema, apod if apod else await APODModel.create(**kwargs))
