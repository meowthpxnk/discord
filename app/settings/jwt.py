from pydantic import Field
from pydantic_settings import BaseSettings


class JWTSettings(BaseSettings):
    access_ttl: int = Field(1800, alias="JWT_ACCESS_TTL")
    refresh_ttl: int = Field(2592000, alias="JWT_REFRESH_TTL")

    max_user_sessions: int = Field(2, alias="JWT_MAX_USER_SESSIONS")
