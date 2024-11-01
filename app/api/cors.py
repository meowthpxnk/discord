import yaml
from pydantic import BaseModel

from app.constants import CORS_CONFIG_PATH
from app.utils.path import read_file


class CorsConfigModel(BaseModel):
    allow_origins: list[str]
    allow_headers: list[str]
    allow_methods: list[str]

    allow_credentials: bool


class CorsConfig:
    def __init__(
        self,
    ) -> None:
        data = read_file(CORS_CONFIG_PATH)
        data = yaml.safe_load(data)
        data = CorsConfigModel.model_validate(data)

        self.config: CorsConfigModel = data

    @property
    def dict(self) -> dict:
        return self.config.model_dump()
