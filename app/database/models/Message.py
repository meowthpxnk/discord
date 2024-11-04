from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app import id_encryptor
from app.schemas import MessageResponseModel

from .__Base import Base


if TYPE_CHECKING:
    from .Chat import Chat
    from .User import User


class MessageForm(BaseModel):
    body: str
    chat_id: Optional[int] = None
    user_id: Optional[int] = None


class Message(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    body: Mapped[str] = mapped_column(String, nullable=False)

    chat_id: Mapped[int] = mapped_column(ForeignKey("chat.id"), nullable=False)
    chat: Mapped["Chat"] = relationship(back_populates="messages")

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"), nullable=False)
    user: Mapped["User"] = relationship(back_populates="messages")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, form: MessageForm) -> None:
        super().__init__(form)

    def jsonify(self) -> MessageResponseModel:
        return MessageResponseModel(
            id=id_encryptor.encrypt_id(self.id),
            user_id=id_encryptor.encrypt_id(self.user_id),
            body=self.body,
            created_at=self.created_at,
        )
