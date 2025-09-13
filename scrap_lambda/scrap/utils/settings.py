from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    model_config=SettingsConfigDict(
        env_file=".env",
        env_file_encoding='utf-8'
    )
    TABLE_NAME: Optional[str] = None
    PROCESS: str
    BUCKET_ERROR_NAME: str
    ACCESS_KEY: Optional[str] = None
    SECRET_ACCESS_KEY: Optional[str] = None


settings=Settings()