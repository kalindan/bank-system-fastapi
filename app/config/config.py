import os
from functools import lru_cache
from pydantic import BaseModel


class Config(BaseModel):
    secret_key: str
    db_url: str


class ProdConfig(Config):
    secret_key: str = os.environ.get("SECRET_KEY", "")
    db_url: str = os.environ.get("DB_URL", "")


class DevConfig(Config):
    secret_key: str = "123456789"
    db_url: str = "sqlite:///database.db"


@lru_cache()
def config() -> Config:
    if os.environ.get("ENV", "production") == "development":
        return DevConfig()
    return ProdConfig()


active_config = config()
