from typing import Optional

from app import id_encryptor
from app.api.routes.__auth_dependencies import (
    CurrentUser,
    UserTokenDataDepends,
    auth_failed_responses,
)
from app.api.routes._base_router import APIRouter
from app.database.errors import NotFoundInDB
from app.database.models import User
from app.schemas import UserDataResponseModel


router = APIRouter(
    tags=["User"],
    dependencies=[UserTokenDataDepends],
    responses=auth_failed_responses,
)


@router.get("/user-data")
def get_user_data(
    user: CurrentUser, user_id: Optional[str] = None
) -> UserDataResponseModel:
    if not user_id:
        return user.jsonify()

    try:
        user_id = id_encryptor.decrypt_id(user_id)
    except:
        raise Exception("Not valid user id")

    try:
        user = User.select_where(User.id == user_id, first=True)
    except NotFoundInDB:
        raise Exception("Not valid user id")

    return user.jsonify()
