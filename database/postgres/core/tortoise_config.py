from config import app_settings

TORTOISE_ORM = {
    "connections": {
        "default": f"postgres://{app_settings.db.postgres_user}:{app_settings.db.postgres_password}"
                   f"@{app_settings.db.postgres_host}:{app_settings.db.postgres_port}"
                   f"/{app_settings.db.postgres_db_name}"
    },
    "apps": {
        "models": {
            "models": [
                "database.postgres.models.apod",
                "database.postgres.models.user",
                "aerich.models",
            ],
            "default_connection": "default",
        }
    }
}
