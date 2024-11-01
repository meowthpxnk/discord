from pydantic import Field
from pydantic_settings import BaseSettings


class ApiSettings(BaseSettings):
    host: str = Field("localhost", alias="API_HOST")
    port: int = Field(2000, alias="API_PORT")
