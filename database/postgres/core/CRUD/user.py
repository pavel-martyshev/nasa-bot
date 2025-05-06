from typing import Type

from tortoise.contrib.pydantic import PydanticModel
from tortoise.models import MODEL

from database.postgres.core.CRUD.base_crud import BaseCrud
from database.postgres.models.user import UserModel
from utils.enums.Schema import Schema


class UserCRUD(BaseCrud):
    @property
    def _model(self) -> Type[MODEL]:
        return UserModel

    @property
    def _schema(self) -> Schema:
        return Schema.UserSchema

    async def get_or_create(self, **kwargs) -> PydanticModel | None:
        user: UserModel | None = await UserModel.get_or_none(telegram_id=kwargs.get("telegram_id"))

        if not user:
            return await self._get_model_schema(Schema.UserSchema, await UserModel.create(**kwargs))

        for key, value in kwargs.items():
            if key == "telegram_id" or key == "last_activity_time":
                continue

            old_value = getattr(user, key, None)

            if value != old_value:
                setattr(user, key, value)

        await user.save()
        return await self._get_model_schema(Schema.UserSchema, user)
