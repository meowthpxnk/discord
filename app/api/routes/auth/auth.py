from datetime import UTC, datetime

from fastapi import HTTPException, Request, Response, status
from fastapi.responses import JSONResponse
from jwt.exceptions import InvalidTokenError

from app import auth_jwt_service, db, logger, settings
from app.api.routes._base_router import APIRouter, ErrorReason
from app.auth.errors import FailedRefreshSession, NotFoundSession
from app.database.errors import AlreadyExistsInDB, NotFoundInDB
from app.database.models.User import User, UserForm
from app.errors import NotValidPassword, NotValidUsernameOrPassword
from app.schemas import UserAuthForm, UserRegForm
from app.utils.hash import check_pw, hash_pw


# TODO: refactor module


router = APIRouter(tags=["Auth"])


FailedAuthResponse = JSONResponse(
    str(NotValidUsernameOrPassword()),
    status_code=status.HTTP_401_UNAUTHORIZED,
)


BAD_TOKEN = HTTPException(
    status_code=status.HTTP_403_FORBIDDEN,
    detail="Not valid refresh token.",
    headers={
        "set-cookie": "Refresh-Token=; Expires=Thu, 01 Jan 1970 00:00:00 GMT; Path=/refresh-session"
    },
)


@router.post(
    "/auth", responses={status.HTTP_401_UNAUTHORIZED: {"model": ErrorReason}}
)
async def auth(form: UserAuthForm, response: Response):
    logger.info(f"Authorisate user, username: {form.username}")
    logger.debug(f"Auth user form: {form}")

    try:
        user = User.select_where(User.username == form.username, first=True)
    except NotFoundInDB:
        return FailedAuthResponse

    try:
        check_pw(form.password, user.password_hash)
    except NotValidPassword:
        return FailedAuthResponse

    access_token, refresh_token = auth_jwt_service.create_session(
        user.username
    )

    response.set_cookie(
        "Refresh-Token",
        refresh_token,
        max_age=settings.jwt.refresh_ttl,
        expires=settings.jwt.refresh_ttl,
        samesite="none",
        secure=True,
        httponly=True,
        path="/refresh-session",
    )

    return {"Access-Token": access_token}


@router.post("/registration")
def registration(form: UserRegForm):
    logger.info(f"Create user, username: {form.username}")
    logger.debug(f"Create user form: {form}")

    try:
        User.exists(User.username == form.username)
    except AlreadyExistsInDB:
        raise Exception(f"Already existed user with username {form.username}")

    hash = hash_pw(form.password)
    form = UserForm(
        username=form.username,
        password_hash=hash,
        # created_at=datetime.now(tz=UTC),
    )

    user = User(form)

    db.session.add(user)
    db.session.commit()


@router.post("/refresh-session")
async def refresh_session(response: Response, request: Request):

    token = request.cookies.get("Refresh-Token")
    if not token:
        raise BAD_TOKEN
    try:
        access_token, refresh_token = auth_jwt_service.refresh_session(
            token.encode()
        )
    except (InvalidTokenError, NotFoundSession, FailedRefreshSession):
        raise BAD_TOKEN

    response.set_cookie(
        "Refresh-Token",
        refresh_token,
        max_age=settings.jwt.refresh_ttl,
        expires=settings.jwt.refresh_ttl,
        samesite="none",
        secure=True,
        httponly=True,
        path="/refresh-session",
    )

    return {"Access-Token": access_token}
