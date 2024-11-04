from typing import Optional, Sequence, Union

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
        responses: Optional[dict[Union[int, str], dict[str, any]]] = None,
    ) -> None:
        base_responses = {status.HTTP_400_BAD_REQUEST: {"model": ErrorReason}}
        if responses:
            base_responses.update(responses)

        super().__init__(
            prefix=prefix,
            tags=tags,
            dependencies=dependencies,
            responses=base_responses,
        )
