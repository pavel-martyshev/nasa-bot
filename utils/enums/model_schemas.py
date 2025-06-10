from enum import Enum

from tortoise.contrib.pydantic import pydantic_model_creator

from database.postgres.models.apod import ApodModel
from database.postgres.models.user import UserModel


class ModelSchemas(Enum):
    """
    Enum container for Pydantic schema instances generated from ORM models.
    """

    APODSchema = pydantic_model_creator(ApodModel)
    UserSchema = pydantic_model_creator(UserModel)
