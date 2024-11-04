from typing import Annotated

from fastapi import Depends, status
from pydantic import BaseModel

from app import auth_jwt_service
from app.database.models import User
from app.schemas import TokenDataSchema


class ErrorReason(BaseModel):
    detailed: str


auth_failed_responses = {
    status.HTTP_401_UNAUTHORIZED: {"model": ErrorReason},
    status.HTTP_403_FORBIDDEN: {"model": ErrorReason},
}


# TODO: refactor module


UserTokenDataDepends = Depends(auth_jwt_service.bearer_authorisation)
TokenData = Annotated[TokenDataSchema, UserTokenDataDepends]


def get_current_user(
    token_data: TokenDataSchema = UserTokenDataDepends,
):
    return User.select_where(User.username == token_data.username, first=True)


CurrentUserDepends = Depends(get_current_user)
CurrentUser = Annotated[User, CurrentUserDepends]
