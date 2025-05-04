from tortoise import Tortoise

from database.postgres.core.tortoise_config import TORTOISE_ORM


async def init_db():
    await Tortoise.init(config=TORTOISE_ORM)
