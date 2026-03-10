"""Measurement router — upload, history, detail, delete."""

import uuid

from fastapi import APIRouter, Depends, File, Form, HTTPException, Query, UploadFile, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.models import User
from app.database import get_db
from app.dependencies import get_current_user
from app.measurement import service
from app.measurement.pipeline import image_to_base64
from app.measurement.schemas import (
    MeasurementDimensions,
    MeasurementListResponse,
    MeasurementResponse,
    MeasurementUploadResponse,
    SessionCreateRequest,
    SessionResponse,
)

router = APIRouter(prefix="/measure", tags=["Measurements"])


# ─── Sessions ──────────────────────────────────────────────────

@router.post("/sessions", response_model=SessionResponse, status_code=status.HTTP_201_CREATED)
async def create_session(
    body: SessionCreateRequest,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Create a calibration session with a reference object."""
    session = await service.create_session(
        db=db,
        user_id=current_user.id,
        reference_object=body.reference_object,
        reference_width_mm=body.reference_width_mm,
        reference_height_mm=body.reference_height_mm,
    )
    return SessionResponse.model_validate(session)


# ─── Upload & Measure ─────────────────────────────────────────

@router.post("/upload", response_model=MeasurementUploadResponse)
async def upload_and_measure(
    image: UploadFile = File(..., description="Photo of the object to measure"),
    reference_height_mm: float = Form(..., description="Reference object height in mm"),
    session_id: uuid.UUID | None = Form(None, description="Optional calibration session ID"),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload a photo and get precise server-side measurements.

    This is the "Photo Mode" endpoint — the full OpenCV pipeline runs on the
    server for maximum accuracy (background removal, edge detection, pixel
    ratio calculation, intersection finding, and distance measurement).
    """
    # Validate file type
    if image.content_type not in ("image/jpeg", "image/png", "image/webp"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, and WebP images are supported",
        )

    # Read file
    image_bytes = await image.read()

    # Validate file size (max 10MB)
    if len(image_bytes) > 10 * 1024 * 1024:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image must be smaller than 10MB",
        )

    try:
        measurement, result = await service.process_and_save_measurement(
            db=db,
            user_id=current_user.id,
            image_bytes=image_bytes,
            reference_height_mm=reference_height_mm,
            session_id=session_id,
        )
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail=str(e),
        )

    # Encode annotated image as base64 for immediate display
    annotated_b64 = None
    if result.annotated_image is not None:
        annotated_b64 = image_to_base64(result.annotated_image)

    return MeasurementUploadResponse(
        measurement=MeasurementResponse.model_validate(measurement),
        dimensions=MeasurementDimensions(
            width_mm=result.width_mm,
            height_mm=result.height_mm,
            area_mm2=result.area_mm2,
            contour_count=result.contour_count,
            horizontal_distances=result.horizontal_distances,
            vertical_distances=result.vertical_distances,
        ),
        annotated_image_base64=annotated_b64,
    )


# ─── History ───────────────────────────────────────────────────

@router.get("/history", response_model=MeasurementListResponse)
async def get_history(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get paginated measurement history for the current user."""
    measurements, total = await service.get_user_measurements(
        db=db,
        user_id=current_user.id,
        page=page,
        page_size=page_size,
    )
    return MeasurementListResponse(
        measurements=[MeasurementResponse.model_validate(m) for m in measurements],
        total=total,
        page=page,
        page_size=page_size,
    )


# ─── Detail ────────────────────────────────────────────────────

@router.get("/{measurement_id}", response_model=MeasurementResponse)
async def get_measurement(
    measurement_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Get a specific measurement by ID."""
    measurement = await service.get_measurement_by_id(
        db=db, measurement_id=measurement_id, user_id=current_user.id
    )
    if not measurement:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found",
        )
    return MeasurementResponse.model_validate(measurement)


# ─── Delete ────────────────────────────────────────────────────

@router.delete("/{measurement_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_measurement(
    measurement_id: uuid.UUID,
    current_user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
):
    """Delete a measurement by ID."""
    deleted = await service.delete_measurement(
        db=db, measurement_id=measurement_id, user_id=current_user.id
    )
    if not deleted:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Measurement not found",
        )
