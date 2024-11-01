from pydantic import Field
from pydantic_settings import BaseSettings


class RedisSettings(BaseSettings):
    host: str = Field("localhost", alias="REDIS_HOST")
    port: int = Field(6379, alias="REDIS_PORT")
