from datetime import datetime

from sqlalchemy import Integer, Text, DateTime, ForeignKey, Float, UniqueConstraint, Index, func
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class TraceabilityLink(Base):
    """A directional link from a source artifact anchor to a target artifact anchor.

    Example: Architecture#C-2 derived_from PRD#FR-3
    Anchors are stable IDs embedded in artifacts (FR-3, C-2, ADR-1, UF-1, E1-S3, ...).
    """

    __tablename__ = "traceability_links"
    __table_args__ = (
        UniqueConstraint(
            "source_file_id", "source_anchor", "target_file_id", "target_anchor", "relation",
            name="uq_trace_link",
        ),
        Index("ix_trace_project", "project_id"),
        Index("ix_trace_source", "source_file_id"),
        Index("ix_trace_target", "target_file_id"),
    )

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    project_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("projects.id", ondelete="CASCADE"), nullable=False
    )
    source_file_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_files.id", ondelete="CASCADE"), nullable=False
    )
    source_anchor: Mapped[str] = mapped_column(Text, nullable=False)
    target_file_id: Mapped[int] = mapped_column(
        Integer, ForeignKey("project_files.id", ondelete="CASCADE"), nullable=False
    )
    target_anchor: Mapped[str] = mapped_column(Text, nullable=False)
    relation: Mapped[str] = mapped_column(
        Text, nullable=False, default="derived_from"
    )  # derived_from | satisfies | conflicts_with | references
    rationale: Mapped[str | None] = mapped_column(Text, nullable=True)
    confidence: Mapped[float] = mapped_column(Float, nullable=False, default=1.0)
    created_by_persona: Mapped[str | None] = mapped_column(Text, nullable=True)
    origin: Mapped[str] = mapped_column(
        Text, nullable=False, default="explicit"
    )  # explicit | suggested | manual
    created_at: Mapped[datetime] = mapped_column(DateTime, server_default=func.now())

    project = relationship("Project")
    source_file = relationship("ProjectFile", foreign_keys=[source_file_id])
    target_file = relationship("ProjectFile", foreign_keys=[target_file_id])
