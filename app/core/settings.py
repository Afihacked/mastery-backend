import os

class Settings:
    APP_NAME: str = "MasterY Backend"
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"

settings = Settings()
