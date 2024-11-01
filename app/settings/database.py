from pydantic import Field
from pydantic_settings import BaseSettings


class DatabaseSettings(BaseSettings):
    uri: str = Field("sqlite:///database.db", alias="DATABASE_URI")
