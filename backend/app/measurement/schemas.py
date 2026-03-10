"""Measurement request/response schemas."""

import uuid
from datetime import datetime

from pydantic import BaseModel, Field


# ─── Session Schemas ───────────────────────────────────────────

class SessionCreateRequest(BaseModel):
    reference_object: str = Field(
        ..., description="Type of reference object", examples=["credit_card", "coin", "custom"]
    )
    reference_width_mm: float = Field(
        ..., gt=0, description="Reference object width in mm"
    )
    reference_height_mm: float = Field(
        ..., gt=0, description="Reference object height in mm"
    )


class SessionResponse(BaseModel):
    id: uuid.UUID
    reference_object: str | None
    reference_width_mm: float | None
    reference_height_mm: float | None
    pixel_ratio: float | None
    created_at: datetime

    model_config = {"from_attributes": True}


# ─── Measurement Schemas ──────────────────────────────────────

class MeasurementDimensions(BaseModel):
    """Dimensions returned from the measurement pipeline."""
    width_mm: float
    height_mm: float
    area_mm2: float
    contour_count: int
    horizontal_distances: list[float]
    vertical_distances: list[float]


class MeasurementResponse(BaseModel):
    id: uuid.UUID
    session_id: uuid.UUID | None
    original_image_url: str | None
    annotated_image_url: str | None
    width_mm: float | None
    height_mm: float | None
    area_mm2: float | None
    unit: str
    mode: str
    metadata_json: dict | None
    created_at: datetime

    model_config = {"from_attributes": True}


class MeasurementUploadResponse(BaseModel):
    measurement: MeasurementResponse
    dimensions: MeasurementDimensions
    annotated_image_base64: str | None = None


class MeasurementListResponse(BaseModel):
    measurements: list[MeasurementResponse]
    total: int
    page: int
    page_size: int
