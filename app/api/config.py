from typing import Optional

import yaml
from pydantic import BaseModel

from app.constants import API_CONFIG_PATH
from app.utils.path import read_file


class TagMetadata(BaseModel):
    name: str
    description: str


class APIConfigModel(BaseModel):
    title: str
    description: str
    version: str
    openapi_tags: Optional[list[TagMetadata]] = None


class APIConfig:
    def __init__(self) -> None:
        data = read_file(API_CONFIG_PATH)
        data = yaml.safe_load(data)
        data = APIConfigModel.model_validate(data)

        self.config: APIConfigModel = data

    @property
    def dict(self):
        return self.config.model_dump()
