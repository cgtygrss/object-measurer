"""Measurement business logic service."""

import io
import os
import uuid
from datetime import datetime

from sqlalchemy import select, func
from sqlalchemy.ext.asyncio import AsyncSession

from app.measurement.models import Measurement, MeasurementSession
from app.measurement.pipeline import (
    MeasurementResult,
    image_to_base64,
    run_measurement_pipeline,
)
from app.config import get_settings

settings = get_settings()


async def create_session(
    db: AsyncSession,
    user_id: uuid.UUID,
    reference_object: str,
    reference_width_mm: float,
    reference_height_mm: float,
) -> MeasurementSession:
    """Create a new calibration session."""
    session = MeasurementSession(
        user_id=user_id,
        reference_object=reference_object,
        reference_width_mm=reference_width_mm,
        reference_height_mm=reference_height_mm,
    )
    db.add(session)
    await db.flush()
    await db.refresh(session)
    return session


async def process_and_save_measurement(
    db: AsyncSession,
    user_id: uuid.UUID,
    image_bytes: bytes,
    reference_height_mm: float,
    session_id: uuid.UUID | None = None,
) -> tuple[Measurement, MeasurementResult]:
    """
    Run the measurement pipeline and save results to DB.

    Returns:
        Tuple of (Measurement record, MeasurementResult data)
    """
    # Run pipeline
    result = run_measurement_pipeline(
        image_bytes=image_bytes,
        reference_height_mm=reference_height_mm,
    )

    # Save original image to local storage
    original_url = await _save_image_locally(image_bytes, "original")

    # Save annotated image
    annotated_url = None
    if result.annotated_image is not None:
        import cv2

        _, annotated_bytes = cv2.imencode(".jpg", result.annotated_image)
        annotated_url = await _save_image_locally(
            annotated_bytes.tobytes(), "annotated"
        )

    # Update session pixel ratio if session exists
    if session_id:
        sess_result = await db.execute(
            select(MeasurementSession).where(MeasurementSession.id == session_id)
        )
        session = sess_result.scalar_one_or_none()
        if session:
            session.pixel_ratio = result.pixel_ratio
            db.add(session)

    # Create measurement record
    measurement = Measurement(
        user_id=user_id,
        session_id=session_id,
        original_image_url=original_url,
        annotated_image_url=annotated_url,
        width_mm=result.width_mm,
        height_mm=result.height_mm,
        area_mm2=result.area_mm2,
        mode="photo",
        metadata_json={
            "contour_count": result.contour_count,
            "horizontal_distances": result.horizontal_distances,
            "vertical_distances": result.vertical_distances,
            "pixel_ratio": result.pixel_ratio,
        },
    )
    db.add(measurement)
    await db.flush()
    await db.refresh(measurement)

    return measurement, result


async def get_user_measurements(
    db: AsyncSession,
    user_id: uuid.UUID,
    page: int = 1,
    page_size: int = 20,
) -> tuple[list[Measurement], int]:
    """Get paginated measurement history for a user."""
    # Count total
    count_result = await db.execute(
        select(func.count(Measurement.id)).where(Measurement.user_id == user_id)
    )
    total = count_result.scalar()

    # Fetch page
    offset = (page - 1) * page_size
    result = await db.execute(
        select(Measurement)
        .where(Measurement.user_id == user_id)
        .order_by(Measurement.created_at.desc())
        .offset(offset)
        .limit(page_size)
    )
    measurements = list(result.scalars().all())

    return measurements, total


async def get_measurement_by_id(
    db: AsyncSession, measurement_id: uuid.UUID, user_id: uuid.UUID
) -> Measurement | None:
    """Get a specific measurement by ID, owned by the user."""
    result = await db.execute(
        select(Measurement).where(
            Measurement.id == measurement_id,
            Measurement.user_id == user_id,
        )
    )
    return result.scalar_one_or_none()


async def delete_measurement(
    db: AsyncSession, measurement_id: uuid.UUID, user_id: uuid.UUID
) -> bool:
    """Delete a measurement owned by the user. Returns True if deleted."""
    measurement = await get_measurement_by_id(db, measurement_id, user_id)
    if not measurement:
        return False
    await db.delete(measurement)
    return True


async def _save_image_locally(image_bytes: bytes, prefix: str) -> str:
    """Save image bytes to local uploads directory. Returns the file path."""
    upload_dir = settings.UPLOAD_DIR
    os.makedirs(upload_dir, exist_ok=True)

    filename = f"{prefix}_{uuid.uuid4().hex[:12]}.jpg"
    filepath = os.path.join(upload_dir, filename)

    with open(filepath, "wb") as f:
        f.write(image_bytes)

    return f"/uploads/{filename}"
