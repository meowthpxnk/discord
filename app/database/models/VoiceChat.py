from datetime import datetime, timezone
from typing import TYPE_CHECKING, Optional

from pydantic import BaseModel
from sqlalchemy import DateTime, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .__Base import Base


if TYPE_CHECKING:
    from .Server import Server


class VoiceChatForm(BaseModel):
    title: str
    server_id: Optional[int] = None


class VoiceChat(Base):
    id: Mapped[int] = mapped_column(primary_key=True)
    title: Mapped[str] = mapped_column(String, nullable=False)

    server_id: Mapped[int] = mapped_column(
        ForeignKey("server.id"), nullable=False
    )
    server: Mapped["Server"] = relationship(back_populates="voice_chats")

    created_at: Mapped[datetime] = mapped_column(
        DateTime, nullable=False, default=lambda: datetime.now(timezone.utc)
    )

    def __init__(self, form: VoiceChatForm) -> None:
        super().__init__(form)
