import os

class Config:
    secret_key: str = os.environ.get("SECRET_KEY", "")
    db_url: str = os.environ.get("DB_URL", "")

    @classmethod
    def create(cls) -> "Config":
        if os.environ.get("ENV", "production") == "development":
            cls.secret_key = "123456789"
            cls.db_url = "sqlite:///database.db"
        return Config()

config = Config.create()
