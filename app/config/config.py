import os
 
class Config:

    def __init__(self):
        if os.environ.get("ENV", "production") == "development":
            self.secret_key = "123456789"
            self.db_url = "sqlite:///database.db"
        else:    
            self.secret_key: str = os.environ.get("SECRET_KEY", "")
            self.db_url: str = os.environ.get("DB_URL", "")
        

config = Config()
