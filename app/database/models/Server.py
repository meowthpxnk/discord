from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import id_encryptor
from app.schemas import ServerResponseModel

from .__Base import Base


if TYPE_CHECKING:
    from .Chat import Chat
    from .ServerUser import ServerUser
    from .User import User
    from .VoiceChat import VoiceChat


class ServerForm(BaseModel):
    title: str


class Server(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False, unique=True)

    chats: Mapped[list["Chat"]] = relationship(back_populates="server")
    voice_chats: Mapped[list["VoiceChat"]] = relationship(
        back_populates="server"
    )
    users: Mapped[list["ServerUser"]] = relationship(back_populates="server")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def jsonify(self) -> ServerResponseModel:
        return ServerResponseModel(
            id=id_encryptor.encrypt_id(self.id),
            title=self.title,
            created_at=self.created_at,
        )

    def __init__(self, form: ServerForm) -> None:
        super().__init__(form)
