from datetime import datetime
from typing import Optional, List
from sqlalchemy import String, Float, DateTime, Integer, JSON, Text
from sqlalchemy.orm import Mapped, mapped_column
from pydantic import BaseModel, Field

from app.database.db import Base


# ─── SQLAlchemy ORM Models ────────────────────────────────────────────

class MeasurementDB(Base):
    __tablename__ = "measurements"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    title: Mapped[str] = mapped_column(String(255), default="Untitled")
    original_image_path: Mapped[str] = mapped_column(String(512))
    result_image_path: Mapped[Optional[str]] = mapped_column(String(512), nullable=True)
    reference_height: Mapped[float] = mapped_column(Float)
    unit: Mapped[str] = mapped_column(String(10), default="cm")
    pixel_ratio: Mapped[Optional[float]] = mapped_column(Float, nullable=True)
    horizontal_measurements: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    vertical_measurements: Mapped[Optional[dict]] = mapped_column(JSON, nullable=True)
    notes: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    created_at: Mapped[datetime] = mapped_column(DateTime, default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )


# ─── Pydantic Schemas ─────────────────────────────────────────────────

class MeasurementCreate(BaseModel):
    title: str = "Untitled"
    reference_height: float = Field(..., gt=0, description="Known height for calibration")
    unit: str = Field(default="cm", pattern="^(mm|cm|m|in|ft)$")
    notes: Optional[str] = None


class MeasurementPoint(BaseModel):
    x: int
    y: int


class MeasurementLine(BaseModel):
    start: MeasurementPoint
    end: MeasurementPoint
    distance: float
    unit: str


class MeasurementResult(BaseModel):
    id: int
    title: str
    original_image_url: str
    result_image_url: Optional[str]
    reference_height: float
    unit: str
    pixel_ratio: Optional[float]
    horizontal_lines: List[MeasurementLine] = []
    vertical_lines: List[MeasurementLine] = []
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True


class MeasurementSummary(BaseModel):
    id: int
    title: str
    result_image_url: Optional[str]
    reference_height: float
    unit: str
    created_at: datetime

    class Config:
        from_attributes = True


class MeasurementUpdate(BaseModel):
    title: Optional[str] = None
    notes: Optional[str] = None
