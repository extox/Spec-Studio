"""Bolt — short, intense work cycles (1–3 hours) derived from sprint planning.

A Bolt is one Story-sized unit of execution with a clear start/complete/approve
lifecycle. All AI activity that occurs while a Bolt is `in_bolt` is captured in
`bolt_activities` so velocity and decision-trace can be reconstructed.
"""

from datetime import datetime

from sqlalchemy import Integer, Text, DateTime, ForeignKey, Boolean, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class Bolt(Base):
    __tablename__ = "bolts"
    __table_args__ = (
        Index("ix_bolt_project", "project_id"),
        Index("ix_bolt_status", "project_id", "status"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    sprint_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    bolt_number: Mapped[int] = mapped_column(Integer, nullable=False)
    title: Mapped[str] = mapped_column(Text, nullable=False)
    story_anchor: Mapped[str | None] = mapped_column(Text, nullable=True)  # e.g. E1-S3
    persona_id: Mapped[str] = mapped_column(Text, nullable=False, default="developer")
    workflow_id: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Text, nullable=False, default="todo"
    )  # todo | in_bolt | awaiting_approval | done | blocked
    started_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    completed_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    estimated_minutes: Mapped[int] = mapped_column(Integer, nullable=False, default=60)
    approval_required: Mapped[bool] = mapped_column(Boolean, nullable=False, default=True)
    approved_by: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    approved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)
    blocker_reason: Mapped[str | None] = mapped_column(Text, nullable=True)
    notes: Mapped[str | None] = mapped_column(Text, nullable=True)
    created_by: Mapped[int] = mapped_column(Integer, ForeignKey("users.id"))
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, server_default=func.now(), onupdate=func.now()
    )

    project = relationship("Project")
    activities = relationship(
        "BoltActivity", back_populates="bolt", cascade="all, delete-orphan"
    )


class BoltActivity(Base):
    """Append-only log of events that occurred during a Bolt."""

    __tablename__ = "bolt_activities"
    __table_args__ = (Index("ix_bact_bolt", "bolt_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    bolt_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("bolts.id", ondelete="CASCADE"), nullable=False
    )
    event_type: Mapped[str] = mapped_column(
        Text, nullable=False
    )  # ai_message | file_saved | checkpoint | approval | status_change | note
    payload: Mapped[str | None] = mapped_column(Text, nullable=True)  # JSON-encoded
    actor_user_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("users.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    bolt = relationship("Bolt", back_populates="activities")
