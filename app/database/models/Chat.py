from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import id_encryptor
from app.schemas import ChatResponseModel

from .__Base import Base


if TYPE_CHECKING:
    from .Message import Message
    from .Server import Server


class ChatForm(BaseModel):
    title: str
    server_id: Optional[int] = None


class Chat(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    server_id: Mapped[int] = mapped_column(
        ForeignKey("server.id"), nullable=False
    )
    server: Mapped["Server"] = relationship(back_populates="chats")

    messages: Mapped[list["Message"]] = relationship(back_populates="chat")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, form: ChatForm) -> None:
        super().__init__(form)

    def jsonify(self) -> ChatResponseModel:
        return ChatResponseModel(
            id=id_encryptor.encrypt_id(self.id),
            title=self.title,
            created_at=self.created_at,
        )
