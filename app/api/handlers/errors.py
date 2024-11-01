import traceback

from fastapi import Request, status
from fastapi.responses import JSONResponse
from starlette.types import Scope
from uvicorn.protocols.utils import get_client_addr, get_path_with_query_string

from app import api, logger


class ScopeHelper:
    def __init__(self, scope: Scope):
        self.addr = get_client_addr(scope)
        self.path = get_path_with_query_string(scope)
        self.method = scope["method"]
        self.version = scope["http_version"]

    def __repr__(self) -> str:
        return f"{self.addr} - {self.method} {self.path} {self.version}"


@api.exception_handler(Exception)
async def exception_handler(request: Request, exc):
    error = str(exc)

    scope = ScopeHelper(request.scope)
    logger.error(
        f"{scope}, reason: {error}, Traceback: {traceback.format_exc()}"
    )

    return JSONResponse(
        {"error": error}, status_code=status.HTTP_400_BAD_REQUEST
    )
