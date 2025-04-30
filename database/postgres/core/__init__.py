from tortoise import Tortoise

from config import app_settings


async def init_db():
    await Tortoise.init(
        db_url=f"postgres://"
               f"{app_settings.db.postgres_user}:{app_settings.db.postgres_password}"
               f"@{app_settings.db.postgres_host}:{app_settings.db.postgres_port}"
               f"/{app_settings.db.postgres_db_name}",
        modules={"models": [
            "database.postgres.models.APOD",
        ]}
    )
