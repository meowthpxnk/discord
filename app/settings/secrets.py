from pydantic import Field
from pydantic_settings import BaseSettings


class SecretsSettings(BaseSettings):
    id_encryptor_secret: str = Field(alias="ID_ENCRYPTOR_SECRET")
