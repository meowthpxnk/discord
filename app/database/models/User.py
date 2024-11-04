from datetime import datetime, timezone
from typing import TYPE_CHECKING

from pydantic import BaseModel
from sqlalchemy import DateTime, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import id_encryptor
from app.schemas import UserDataResponseModel

from .__Base import Base


if TYPE_CHECKING:
    from .Message import Message
    from .ServerUser import ServerUser


class UserForm(BaseModel):
    username: str
    password_hash: str


class User(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)

    messages: Mapped[list["Message"]] = relationship(back_populates="user")
    servers: Mapped[list["ServerUser"]] = relationship(back_populates="user")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, form: UserForm) -> None:
        super().__init__(form)

    def jsonify(self) -> UserDataResponseModel:
        return UserDataResponseModel(
            id=id_encryptor.encrypt_id(self.id),
            username=self.username,
            created_at=self.created_at,
        )
