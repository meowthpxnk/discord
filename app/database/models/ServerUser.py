import enum
from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import (
    Column,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    String,
    Table,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .__Base import Base


if TYPE_CHECKING:
    from .Server import Server
    from .User import User


class ServerUserRoleEnum(enum.Enum):
    OWNER = "OWNER"
    USER = "USER"


class ServerUserForm(BaseModel):
    role: ServerUserRoleEnum

    user_id: Optional[int] = None
    server_id: Optional[int] = None


class ServerUser(Base):
    server_id: Mapped[int] = mapped_column(
        ForeignKey("server.id"), primary_key=True, nullable=False
    )
    server: Mapped["Server"] = relationship(back_populates="users")

    user_id: Mapped[int] = mapped_column(
        ForeignKey("user.id"), primary_key=True, nullable=False
    )
    user: Mapped["User"] = relationship(back_populates="servers")

    role: Mapped[ServerUserRoleEnum] = mapped_column(
        Enum(ServerUserRoleEnum),
        nullable=False,
        default=ServerUserRoleEnum.USER,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, form: ServerUserForm) -> None:
        super().__init__(form)
