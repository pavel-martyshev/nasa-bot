from abc import ABC, abstractmethod
from typing import Dict, Any, Type

from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import MODEL
from tortoise.transactions import atomic

from utils.enums.Schema import Schema


class BaseCrud(ABC):
    @property
    @abstractmethod
    def _model(self) -> Type[MODEL]:
        pass

    @property
    @abstractmethod
    def _schema(self) -> Schema:
        pass

    @staticmethod
    async def _get_model_schema(schema: Schema, db_model: MODEL) -> PydanticModel | None:
        if db_model is None:
            return None

        return await schema.value.from_tortoise_orm(db_model)

    @atomic()
    async def get(self, **kwargs) -> PydanticModel | None:
        model: MODEL | None = await self._model.get_or_none(**kwargs)

        if model:
            return await self._get_model_schema(self._schema, model)

        return None

    @atomic()
    async def get_or_create(self, **kwargs) -> PydanticModel | None:
        return await self._get_model_schema(self._schema, (await self._model.get_or_create(**kwargs))[0])

    @atomic()
    async def update(
            self,
            *,
            filters: Dict[str, Any],
            **kwargs
    ) -> PydanticModel | bool:
        model: MODEL | None = await self._model.get_or_none(**filters)

        if not model:
            return False

        for key, value in kwargs.items():
            old_value = getattr(model, key, None)

            if value != old_value:
                setattr(model, key, value)

        await model.save()
        return await self._get_model_schema(self._schema, model)

    @atomic()
    async def exists(self, **kwargs) -> bool:
        return await self._model.exists(**kwargs)
