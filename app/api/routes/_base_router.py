from typing import Sequence

from fastapi import APIRouter, Depends, status
from pydantic import BaseModel


class ErrorReason(BaseModel):
    error: str


class APIRouter(APIRouter):
    def __init__(
        self,
        tags: list[str] = None,
        prefix: str = "",
        dependencies: Sequence[Depends] = None,
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses={status.HTTP_400_BAD_REQUEST: {"model": ErrorReason}},
        )
