from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings


class LoggerLevel(Enum):
    INFO = "INFO"
    DEBUG = "DEBUG"


class LoggerSettings(BaseSettings):
    level: LoggerLevel = Field(LoggerLevel.INFO, alias="LOGGER_LEVEL")
