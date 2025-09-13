from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config=SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
    SECRET_KEY: str
    ALGORITHM: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    MYSQL_USER: str
    MYSQL_PASSWORD: str
    MYSQL_HOST: str
    MYSQL_PORT: str
    MYSQL_DATABASE: str
settings = Settings()

#class Settings_dev(BaseSettings):
#    model_config=SettingsConfigDict(env_file='.env', env_file_encoding='utf-8')
#    DATABASE_URL: str
#    SECRET_KEY: str
#    ALGORITHM: str
#    ACCESS_TOKEN_EXPIRE_MINUTES: int
#settings = Settings_dev()