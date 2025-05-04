from tortoise import BaseDBAsyncClient


async def upgrade(db: BaseDBAsyncClient) -> str:
    return """
        CREATE TABLE IF NOT EXISTS "apod" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "created_at" BIGINT NOT NULL,
    "is_deleted" BOOL NOT NULL DEFAULT False,
    "title" VARCHAR(100) NOT NULL,
    "title_ru" VARCHAR(100) NOT NULL,
    "date" DATE NOT NULL,
    "explanation" TEXT NOT NULL,
    "explanation_ru" TEXT NOT NULL,
    "url" VARCHAR(150) NOT NULL,
    "hdurl" VARCHAR(150),
    "media_type" VARCHAR(15) NOT NULL
);
CREATE TABLE IF NOT EXISTS "aerich" (
    "id" SERIAL NOT NULL PRIMARY KEY,
    "version" VARCHAR(255) NOT NULL,
    "app" VARCHAR(100) NOT NULL,
    "content" JSONB NOT NULL
);"""


async def downgrade(db: BaseDBAsyncClient) -> str:
    return """
        """
