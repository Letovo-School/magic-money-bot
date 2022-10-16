from functools import cache

import orjson
from pydantic import BaseSettings, BaseConfig

BaseConfig.json_loads = orjson.loads
BaseConfig.json_dumps = orjson.dumps


class AppSettings(BaseSettings):
    TG_API_ID: int
    TG_API_HASH: str
    TG_BOT_TOKEN: str
    # DATABASE_URL: PostgresDsn
    production: bool = True

    class Config:
        env_file = ".env.local"
        env_file_encoding = "utf-8"


@cache
def settings() -> AppSettings:
    """
    ``settings.cache_clear()`` to dump cache
    """
    return AppSettings()
