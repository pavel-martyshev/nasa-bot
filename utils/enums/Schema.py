from enum import Enum

from tortoise.contrib.pydantic import pydantic_model_creator

from database.postgres.models.apod import APODModel
from database.postgres.models.user import UserModel


class Schema(Enum):
    APODSchema = pydantic_model_creator(APODModel)
    UserSchema = pydantic_model_creator(UserModel)
