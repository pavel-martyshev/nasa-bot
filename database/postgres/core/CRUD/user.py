from typing import Any

from tortoise.contrib.pydantic import PydanticModel

from database.postgres.core.CRUD.base_crud import BaseCrud
from database.postgres.models.user import UserModel
from utils.enums.model_schemas import ModelSchemas


class UserCrud(BaseCrud):
    """
    CRUD operations for the User model.
    """

    @property
    def _model(self) -> type[UserModel]:
        return UserModel

    @property
    def _schema(self) -> ModelSchemas:
        return ModelSchemas.UserSchema

    async def get_or_create(self, **kwargs: Any) -> PydanticModel | None:
        """
        Retrieve a user by telegram_id or create a new one.
        If found, updates the user with new values except 'telegram_id' and 'last_activity_time'.

        Args:
            **kwargs (Any): Fields for lookup and optional update or creation.

        Returns:
            PydanticModel | None: Serialized user instance.
        """
        user: UserModel | None = await UserModel.get_or_none(telegram_id=kwargs.get("telegram_id"))

        if not user:
            return await self._get_model_schema(ModelSchemas.UserSchema, await UserModel.create(**kwargs))

        for key, value in kwargs.items():
            if key == "telegram_id" or key == "last_activity_time":
                continue

            old_value = getattr(user, key, None)

            if value != old_value:
                setattr(user, key, value)

        await user.save()
        return await self._get_model_schema(ModelSchemas.UserSchema, user)
