from app.schemas import JWTTokenTypeEnum


class NotFoundSession(Exception):
    def __init__(self, username: str, session_id: str) -> None:
        super().__init__(
            f"Not found session with username {username} id {session_id}, in session storage."
        )


class NotValidSession(Exception):
    def __init__(self, username: str, session_id: str) -> None:
        super().__init__(
            f"Not valid session with username {username} id {session_id}."
        )


class NotValidTokenType(Exception):
    def __init__(
        self, current_type: JWTTokenTypeEnum, expected_type: JWTTokenTypeEnum
    ) -> None:
        super().__init__(
            f"Not valid token type, current type is {current_type}, but expected is {expected_type}"
        )


class FailedRefreshSession(Exception):
    def __init__(self) -> None:
        super().__init__("Failed refresh session.")
