"""Spec Validation Engine — runs and issues."""

from datetime import datetime

from sqlalchemy import Integer, Text, DateTime, Float, ForeignKey, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class ValidationRun(Base):
    """One execution of the validation engine over a project (or scope)."""

    __tablename__ = "validation_runs"
    __table_args__ = (Index("ix_vrun_project", "project_id"),)

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    scope: Mapped[str] = mapped_column(Text, nullable=False, default="all")  # all | file | cross-doc
    file_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("project_files.id", ondelete="SET NULL"), nullable=True
    )
    triggered_by: Mapped[str] = mapped_column(
        Text, nullable=False, default="manual"
    )  # manual | auto-on-save | scheduled
    status: Mapped[str] = mapped_column(Text, nullable=False, default="completed")
    duration_ms: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    rules_executed: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    issues_open: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    issues_resolved: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    health_score: Mapped[float] = mapped_column(Float, nullable=False, default=100.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    project = relationship("Project")
    issues = relationship(
        "ValidationIssue", back_populates="run", cascade="all, delete-orphan"
    )


class ValidationIssue(Base):
    __tablename__ = "validation_issues"
    __table_args__ = (
        Index("ix_vissue_project", "project_id"),
        Index("ix_vissue_status", "project_id", "status"),
        Index("ix_vissue_file", "file_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    run_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("validation_runs.id", ondelete="CASCADE"), nullable=False
    )
    rule_id: Mapped[str] = mapped_column(Text, nullable=False)
    severity: Mapped[str] = mapped_column(Text, nullable=False)  # error | warning | info
    file_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("project_files.id", ondelete="SET NULL"), nullable=True
    )
    anchor: Mapped[str | None] = mapped_column(Text, nullable=True)
    related_file_id: Mapped[int | None] = mapped_column(
        Integer, ForeignKey("project_files.id", ondelete="SET NULL"), nullable=True
    )
    related_anchor: Mapped[str | None] = mapped_column(Text, nullable=True)
    message: Mapped[str] = mapped_column(Text, nullable=False)
    suggestion: Mapped[str | None] = mapped_column(Text, nullable=True)
    status: Mapped[str] = mapped_column(
        Text, nullable=False, default="open"
    )  # open | acknowledged | resolved | suppressed
    fingerprint: Mapped[str] = mapped_column(Text, nullable=False)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())
    resolved_at: Mapped[datetime | None] = mapped_column(DateTime, nullable=True)

    run = relationship("ValidationRun", back_populates="issues")
