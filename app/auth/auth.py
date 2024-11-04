import os
from datetime import UTC, datetime, timedelta
from uuid import uuid4

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import InvalidTokenError

from app import redis_client, settings
from app.constants import (
    JWT_ALGORITHM,
    JWT_FOLDER_PATH,
    JWT_PRIVATE_NAME,
    JWT_PUBLIC_NAME,
)
from app.schemas import JWTTokenTypeEnum, TokenDataSchema, TokenPayloadSchema

from .errors import (
    FailedRefreshSession,
    NotFoundSession,
    NotValidSession,
    NotValidTokenType,
)


# TODO:!!!  refactor module


class AuthJWTService:
    private_key: bytes
    public_key: bytes

    @staticmethod
    def _gen_session_id() -> str:
        return str(uuid4())

    def _set_keys(self):
        with open(os.path.join(JWT_FOLDER_PATH, JWT_PRIVATE_NAME), "rb") as f:
            self.private_key = f.read()

        with open(os.path.join(JWT_FOLDER_PATH, JWT_PUBLIC_NAME), "rb") as f:
            self.public_key = f.read()

    def encode(self, payload: TokenPayloadSchema) -> tuple[str, str]:
        now = datetime.now(UTC)

        access_payload = TokenDataSchema(
            **payload.model_dump(),
            type=JWTTokenTypeEnum.ACCESS,
            exp=jwt.api_jwt.timegm(
                (
                    now + timedelta(seconds=settings.jwt.access_ttl)
                ).utctimetuple()
            ),
        ).model_dump(mode="json")

        access_token = jwt.encode(
            access_payload,
            key=self.private_key,
            algorithm=JWT_ALGORITHM,
        )

        refresh_payload = TokenDataSchema(
            **payload.model_dump(),
            type=JWTTokenTypeEnum.REFRESH,
            exp=jwt.api_jwt.timegm(
                (
                    now + timedelta(seconds=settings.jwt.refresh_ttl)
                ).utctimetuple()
            ),
        ).model_dump(mode="json")

        refresh_token = jwt.encode(
            refresh_payload,
            key=self.private_key,
            algorithm=JWT_ALGORITHM,
        )

        return access_token, refresh_token

    def decode(self, token: str) -> TokenDataSchema:
        data = jwt.decode(token, self.public_key, algorithms=[JWT_ALGORITHM])
        return TokenDataSchema(**data)

    def bearer_authorisation(
        self,
        http_bearer: HTTPAuthorizationCredentials = Depends(HTTPBearer()),
    ):
        try:
            data = self.decode(http_bearer.credentials)
        except InvalidTokenError:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )

        try:
            self.validate_session(data.username, data.session_id)
        except NotValidSession:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not valid token session.",
            )
        return data

    def refresh_session(self, refresh_token: bytes) -> tuple[str, str]:
        data = self.decode(refresh_token)

        if not data.type == JWTTokenTypeEnum.REFRESH:
            raise NotValidTokenType(data.type, JWTTokenTypeEnum.REFRESH)

        session_token = self.get_session_token(data.username, data.session_id)

        if not session_token == refresh_token:
            self.close_session(data.username, data.session_id)
            raise FailedRefreshSession

        access_token, refresh_token = self.create_session(
            data.username, data.session_id
        )

        return access_token, refresh_token

    def get_session_token(self, username: str, session_id: str) -> str:

        # id = redis_client.session_service.get_user_session_pattern(
        #     username, session_id
        # )
        token = redis_client.session_service.get(username, session_id)

        if token == None:
            raise NotFoundSession(username, session_id)
        return token

    def close_sessions(
        self, username: str, exclude_session_id: str = None
    ) -> None:
        keys = redis_client.session_service.get_user_session_keys(username)

        if exclude_session_id:
            exclude_session_key = (
                redis_client.session_service.get_user_session_pattern(
                    username, exclude_session_id
                )
            )

            keys = list(filter(lambda key: key != exclude_session_key, keys))

        for key in keys:
            redis_client.session_service.delete(key)

    def validate_session(self, username: str, session_id: str) -> None:
        try:
            self.get_session_token(username, session_id)
        except NotFoundSession:
            raise NotValidSession(username, session_id)

    def get_sessions(self, username: str) -> list[str]:
        keys = redis_client.session_service.get_user_session_keys(username)
        return [redis_client.session_service.get_by_key(key) for key in keys]

    def get_session_data(self, token: bytes) -> TokenDataSchema:
        return self.decode(token)

    def create_session(
        self, username: str, session_id: str = None
    ) -> tuple[str, str]:

        if session_id == None:
            previous_sessions = self.get_sessions(username)

            # TODO: remove all sessions if more than max value

            if len(previous_sessions) >= settings.jwt.max_user_sessions:
                previous_sessions = [
                    self.get_session_data(key) for key in previous_sessions
                ]
                previous_sessions.sort(key=lambda session: session.exp)

                session_to_close = previous_sessions[0]

                self.close_session(
                    session_to_close.username, session_to_close.session_id
                )

            session_id = self._gen_session_id()

        access_token, refresh_token = self.encode(
            payload=TokenPayloadSchema(
                username=username, session_id=session_id
            )
        )

        redis_client.session_service.set(username, refresh_token, session_id)

        return access_token, refresh_token

    def close_session(self, username: str, session_id: str) -> None:
        id = redis_client.session_service.get_user_session_pattern(
            username, session_id
        )
        redis_client.session_service.delete(id)
