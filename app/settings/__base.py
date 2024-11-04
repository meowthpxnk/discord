from dotenv import load_dotenv
from pydantic_settings import BaseSettings

from .api import ApiSettings
from .database import DatabaseSettings
from .jwt import JWTSettings
from .logger import LoggerSettings
from .redis import RedisSettings
from .secrets import SecretsSettings


load_dotenv()


class Settings(BaseSettings):
    database: DatabaseSettings = DatabaseSettings()
    logger: LoggerSettings = LoggerSettings()
    api: ApiSettings = ApiSettings()
    redis: RedisSettings = RedisSettings()
    jwt: JWTSettings = JWTSettings()
    secrets: SecretsSettings = SecretsSettings()
