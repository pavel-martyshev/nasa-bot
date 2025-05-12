from abc import ABC, abstractmethod
from typing import Any

from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import Model
from tortoise.transactions import atomic

from utils.enums.model_schemas import ModelSchemas


class BaseCrud(ABC):
    """
    Abstract base class for CRUD operations on Tortoise ORM models.

    Subclasses must define:
        - _model: ORM model class.
        - _schema: Corresponding Pydantic schema (as a Schema enum).
    """
    @property
    @abstractmethod
    def _model(self) -> type[Model]:
        pass

    @property
    @abstractmethod
    def _schema(self) -> ModelSchemas:
        pass

    @staticmethod
    async def _get_model_schema(schema: ModelSchemas, db_model: Model) -> PydanticModel | None:
        """
        Convert a Tortoise ORM model instance to its corresponding Pydantic schema.

        Args:
            schema (ModelSchemas): Enum containing the Pydantic schema.
            db_model (Model): ORM model instance.

        Returns:
            PydanticModel | None: Serialized model or None if input is None.
        """
        if db_model is None:
            return None

        return await schema.value.from_tortoise_orm(db_model)

    @atomic()
    async def get(self, **kwargs: Any) -> PydanticModel | None:
        """
        Retrieve a single model instance matching the given filters.

        Args:
            **kwargs (Any): Filters to apply when querying the model.

        Returns:
            PydanticModel | None: Serialized model or None if not found.
        """
        model: Model | None = await self._model.get_or_none(**kwargs)

        if model:
            return await self._get_model_schema(self._schema, model)

        return None

    @atomic()
    async def get_or_create(self, **kwargs: Any) -> PydanticModel | None:
        """
        Retrieve an existing model or create a new one if not found.

        Args:
            **kwargs (Any): Fields used for lookup and creation.

        Returns:
            PydanticModel | None: Serialized model.
        """
        return await self._get_model_schema(self._schema, (await self._model.get_or_create(**kwargs))[0])

    @atomic()
    async def update(
            self,
            *,
            filters: dict[str, Any],
            **kwargs: Any
    ) -> PydanticModel | bool:
        """
        Update an existing model instance with new values.

        Args:
            filters (dict[str, Any]): Fields to locate the model instance.
            **kwargs (Any): Fields and values to update.

        Returns:
            PydanticModel | bool: Updated model if successful, False if not found or serialization failed.
        """
        model: Model | None = await self._model.get_or_none(**filters)

        if not model:
            return False

        for key, value in kwargs.items():
            old_value = getattr(model, key, None)

            if value != old_value:
                setattr(model, key, value)

        await model.save()

        schema: PydanticModel | None = await self._get_model_schema(self._schema, model)

        if schema is None:
            return False

        return schema

    @atomic()
    async def exists(self, **kwargs: Any) -> bool:
        """
        Check if any model instance exists matching the given filters.

        Args:
            **kwargs (Any): Filters to apply.

        Returns:
            bool: True if at least one match is found, else False.
        """
        return await self._model.exists(**kwargs)
