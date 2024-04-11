from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    load_dotenv(override=True)
    model_config = SettingsConfigDict(env_file="./.env")

    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    DB_PASSWORD: str
    DB_USER: str

    @property
    def get_pg_connection(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"


settings = Settings()

