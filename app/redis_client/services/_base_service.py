from abc import ABC
from typing import TYPE_CHECKING

from ..errors import NotFoundInRedis, NotValidPattern


if TYPE_CHECKING:
    from ..redis_client import Redis


class BaseRedisService(ABC):
    pattern: str

    name: str

    def __init__(self, redis_client: "Redis") -> None:
        self.redis_client: "Redis" = redis_client

    @classmethod
    def _get_pattern(cls) -> str:
        try:
            return cls.pattern
        except:
            raise NotValidPattern(cls.__class__.__name__)

    @classmethod
    def _current_name(cls, id: str) -> str:
        return cls._get_pattern + id

    def get(self, id: str) -> bytes:
        name = self._current_name(id)
        value = self.redis_client.get(name)
        if not value:
            raise NotFoundInRedis(self.__class__.__name__, id)
        return value

    def set(self, id: str, value: str, ex: int = None) -> None:
        name = self._current_name(id)
        self.redis_client.set(name, value, ex)

    def delete(self, id: str) -> None:
        name = self._current_name(id)
        self.redis_client.delete(name)

    def keys(self) -> list[str]:
        pattern = self._get_pattern() + "*"
        return self.redis_client.keys(pattern)
