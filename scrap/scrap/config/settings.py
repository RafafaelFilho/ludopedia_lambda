from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Literal

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    DB_TYPE: Literal['mysql', 'sqlite']
    # MySQL configs
    MYSQL_USER: str = ''
    MYSQL_PASSWORD: str = ''
    MYSQL_HOST: str = ''
    MYSQL_PORT: str = ''
    MYSQL_DATABASE: str = ''
    # sqlite config
    SQLITE_PATH: str = ''
    # sentry
    SENTRY_DSN: str

    @property
    def database_url(self) -> str:
        if self.db_type=='mysql':
            return f"mysql+pymysql://{self.MYSQL_USER}:{self.MYSQL_PASSWORD}@{self.MYSQL_HOST}:{self.MYSQL_PORT}/{self.MYSQL_DATABASE}"
        elif self.db_type=='sqlite':
            return f'sqlite:///{self.SQLITE_PATH}'

settings=Settings()