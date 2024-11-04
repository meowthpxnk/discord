from pydantic import BaseModel
from sqlalchemy import select
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import DeclarativeBase, Mapped
from sqlalchemy.sql._typing import _ColumnExpressionArgument

from app import logger
from app.utils.camel_to_snake import camel_to_snake

from ..errors import AlreadyExistsInDB, NotFoundInDB


class Base(DeclarativeBase):
    id: Mapped[int]

    @declared_attr
    def __tablename__(cls) -> str:
        return camel_to_snake(cls.__name__)

    @classmethod
    def select_where(
        cls,
        *whereclause: _ColumnExpressionArgument[bool],
        first: bool = False,
    ):  # noqa: ANN206
        from .. import session

        stmt = select(cls).where(*whereclause)

        if not first:
            return session.scalars(stmt).all()

        item = session.scalars(stmt).first()

        if item is None:
            raise NotFoundInDB(whereclause, cls.__name__)

        return item

    @classmethod
    def exists(cls, *whereclause: _ColumnExpressionArgument[bool]) -> None:
        try:
            cls.select_where(*whereclause, first=True)
        except NotFoundInDB:
            pass
        else:
            raise AlreadyExistsInDB(whereclause, cls.__name__)

    def jsonify(self) -> BaseModel:
        raise NotImplementedError

    def __init__(self, form: BaseModel) -> None:
        for k, v in form.model_dump().items():
            try:
                self.__setattr__(k, v)
            except AttributeError as err:
                logger.error(err)
                pass

    def __repr__(self) -> str:
        return f"<{self.__class__.__name__} ID: {self.id}>"
