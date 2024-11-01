import yaml
from pydantic import BaseModel

from app.constants import BASE_CONFIG_PATH
from app.utils.path import read_file


class BaseConfigModel(BaseModel):
    title: str
    description: str


class BaseConfig:
    def __init__(self):
        data = read_file(BASE_CONFIG_PATH)
        data = yaml.safe_load(data)
        data = BaseConfigModel.model_validate(data)

        self.config: BaseConfigModel = data

    @property
    def dict(self):
        return self.config.model_dump()
