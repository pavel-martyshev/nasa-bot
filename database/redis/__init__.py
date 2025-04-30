from aiogram.fsm.storage.base import DefaultKeyBuilder
from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

from config import app_settings

redis = Redis(
    host=app_settings.db.redis_host,
    port=app_settings.db.redis_port,
    db=app_settings.db.redis_db_number,
)
storage = RedisStorage(redis, key_builder=DefaultKeyBuilder(prefix="nasa-bot", with_destiny=True))
