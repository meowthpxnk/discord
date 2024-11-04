from app import settings

from ._base_service import BaseRedisService


# TODO:!!!  refactor module


class SessionService(BaseRedisService):
    pattern = "UserSession."

    def set(
        self,
        username: str,
        value: str,
        session_id: str,
    ) -> None:
        name = self.get_user_session_pattern(username, session_id)
        name = name.replace(self.pattern, "")
        super().set(name, value, settings.jwt.refresh_ttl)

    def get(self, username: str, session_id: str):
        name = self.get_user_session_pattern(username, session_id)
        name = name.replace(self.pattern, "")

        return super().get(name)

    def delete(self, key: str):
        if isinstance(key, bytes):
            key = key.decode()
        name = key.replace(self.pattern, "")

        return super().delete(name)

    def get_by_key(self, key: str):
        if isinstance(key, bytes):
            key = key.decode()
        name = key.replace(self.pattern, "")

        return super().get(name)

    @classmethod
    def get_user_pattern(cls, username: str) -> str:
        return cls.pattern + f"{username}"

    @classmethod
    def get_user_session_pattern(cls, username: str, session_id: str) -> str:
        return f"{cls.get_user_pattern(username)}.{session_id}"

    def get_user_session_keys(self, username: str) -> list[str]:
        return self.keys(self.get_user_pattern(username))

    def keys(self, pattern: str) -> list[str]:
        return self.redis_client.keys(pattern + "*")
