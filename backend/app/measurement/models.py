"""Measurement and session database models."""

import uuid
from datetime import datetime

from sqlalchemy import DateTime, Float, ForeignKey, JSON, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database import Base


class MeasurementSession(Base):
    """A calibration session with a reference object."""

    __tablename__ = "measurement_sessions"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    reference_object: Mapped[str | None] = mapped_column(String(100))
    reference_width_mm: Mapped[float | None] = mapped_column(Float)
    reference_height_mm: Mapped[float | None] = mapped_column(Float)
    pixel_ratio: Mapped[float | None] = mapped_column(Float)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    user = relationship("User", back_populates="sessions")
    measurements = relationship(
        "Measurement", back_populates="session", cascade="all, delete-orphan"
    )


class Measurement(Base):
    """A single object measurement result."""

    __tablename__ = "measurements"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )
    session_id: Mapped[uuid.UUID | None] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("measurement_sessions.id", ondelete="CASCADE"),
        nullable=True,
    )
    user_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("users.id", ondelete="CASCADE"), index=True
    )
    original_image_url: Mapped[str | None] = mapped_column(Text)
    annotated_image_url: Mapped[str | None] = mapped_column(Text)
    width_mm: Mapped[float | None] = mapped_column(Float)
    height_mm: Mapped[float | None] = mapped_column(Float)
    area_mm2: Mapped[float | None] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10), default="mm")
    mode: Mapped[str] = mapped_column(String(20), default="photo")
    metadata_json: Mapped[dict | None] = mapped_column(JSON, nullable=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow
    )

    # Relationships
    session = relationship("MeasurementSession", back_populates="measurements")
    user = relationship("User", back_populates="measurements")
