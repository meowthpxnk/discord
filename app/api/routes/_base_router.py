from typing import Sequence

from fastapi import APIRouter, Depends
from pydantic import BaseModel


class ErrorReason(BaseModel):
    error: str


class APIRouter(APIRouter):
    def __init__(
        self,
        tags: list[str] = None,
        prefix=None,
        dependencies: Sequence[Depends] = None,
    ) -> None:
        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses={400: {"model": ErrorReason}},
        )
