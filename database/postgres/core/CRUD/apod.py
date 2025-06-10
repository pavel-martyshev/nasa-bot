from typing import Any

from tortoise.contrib.pydantic import PydanticModel

from database.postgres.core.CRUD.base_crud import BaseCrud
from database.postgres.models.apod import ApodModel
from utils.enums.model_schemas import ModelSchemas


class ApodCrud(BaseCrud):
    """
    CRUD operations for the APOD model.
    """

    @property
    def _model(self) -> type[ApodModel]:
        return ApodModel

    @property
    def _schema(self) -> ModelSchemas:
        return ModelSchemas.APODSchema

    async def get_or_create(self, **kwargs: Any) -> PydanticModel | None:
        """
        Retrieve an existing APOD entry by date or create a new one.

        Args:
            **kwargs (Any): Must include 'date' and other fields required for creation.

        Returns:
            PydanticModel | None: Serialized APOD model instance or None if creation failed.
        """
        apod: ApodModel | None = await ApodModel.get_or_none(date=kwargs.get("date"))
        return await self._get_model_schema(ModelSchemas.APODSchema, apod if apod else await ApodModel.create(**kwargs))
