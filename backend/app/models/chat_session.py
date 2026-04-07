from datetime import datetime

from sqlalchemy import Integer, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ChatSession(Base):
    __tablename__ = "chat_sessions"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(Integer, ForeignKey("projects.id", ondelete="CASCADE"))
    persona: Mapped[str] = mapped_column(Text, nullable=False)
    workflow: Mapped[str | None] = mapped_column(Text, nullable=True)
    workflow_step: Mapped[int] = mapped_column(Integer, default=0)
    title: Mapped[str | None] = mapped_column(Text, nullable=True)
    external_conversation_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    project = relationship("Project", back_populates="chat_sessions")
    creator = relationship("User", back_populates="chat_sessions_created")
    messages = relationship("ChatMessage", back_populates="session", cascade="all, delete-orphan")
    files_created = relationship("ProjectFile", back_populates="session")
