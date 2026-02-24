import os
import uuid
from io import BytesIO
from datetime import datetime

from fastapi import APIRouter, UploadFile, File, Form, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.db import get_db
from app.models.measurement import (
    MeasurementDB,
    MeasurementResult,
    MeasurementLine,
    MeasurementPoint,
)
from app.services.background_removal import remove_background
from app.services.edge_detection import detect_edges
from app.services.intersection import find_intersections
from app.services.pixel_ratio import calculate_pixel_ratio
from app.services.measurement import measure_object

router = APIRouter(prefix="/api/measure", tags=["Measurement"])


@router.post("/", response_model=MeasurementResult)
async def create_measurement(
    image: UploadFile = File(..., description="Image of the object to measure"),
    title: str = Form(default="Untitled"),
    reference_height: float = Form(..., gt=0, description="Known reference height"),
    unit: str = Form(default="cm"),
    interval: int = Form(default=20, ge=5, le=100),
    notes: str = Form(default=None),
    db: AsyncSession = Depends(get_db),
):
    """
    Upload an image, process it, and return measurements.

    Pipeline:
    1. Remove background
    2. Detect edges and contours
    3. Find grid intersection points
    4. Calculate pixel ratio from reference height
    5. Measure all distances
    6. Return annotated image + structured data
    """
    # Validate file type
    if image.content_type not in ["image/jpeg", "image/png", "image/webp"]:
        raise HTTPException(400, "Only JPEG, PNG, and WebP images are supported")

    image_bytes = await image.read()
    if len(image_bytes) > settings.MAX_UPLOAD_SIZE:
        raise HTTPException(400, f"Image exceeds max size of {settings.MAX_UPLOAD_SIZE // 1024 // 1024}MB")

    # Generate unique filenames
    file_id = str(uuid.uuid4())
    ext = os.path.splitext(image.filename or "image.jpg")[1] or ".jpg"
    original_filename = f"{file_id}_original{ext}"
    result_filename = f"{file_id}_result.png"

    # Save original
    original_path = os.path.join(settings.UPLOAD_DIR, original_filename)
    with open(original_path, "wb") as f:
        f.write(image_bytes)

    try:
        # ── Processing Pipeline ──────────────────────────────────────
        # 1. Remove background
        img_no_bg = remove_background(image_bytes)

        # 2. Edge detection
        img_annotated, contours = detect_edges(img_no_bg)

        if not contours:
            raise HTTPException(422, "No objects detected in the image. Try with better lighting or contrast.")

        # 3. Find intersections
        h_intersections, v_intersections = find_intersections(contours, interval)

        # 4. Calculate pixel ratio
        pixel_ratio = calculate_pixel_ratio(contours, interval, reference_height)

        # 5. Measure and annotate
        result_image, h_lines, v_lines = measure_object(
            img_annotated, h_intersections, v_intersections, pixel_ratio, unit
        )

        # Save result image
        result_path = os.path.join(settings.RESULTS_DIR, result_filename)
        result_image.save(result_path, "PNG")

        # ── Persist to DB ────────────────────────────────────────────
        h_data = [line.model_dump() for line in h_lines]
        v_data = [line.model_dump() for line in v_lines]

        db_measurement = MeasurementDB(
            title=title,
            original_image_path=original_filename,
            result_image_path=result_filename,
            reference_height=reference_height,
            unit=unit,
            pixel_ratio=pixel_ratio,
            horizontal_measurements=h_data,
            vertical_measurements=v_data,
            notes=notes,
        )
        db.add(db_measurement)
        await db.flush()
        await db.refresh(db_measurement)

        return MeasurementResult(
            id=db_measurement.id,
            title=db_measurement.title,
            original_image_url=f"/static/uploads/{original_filename}",
            result_image_url=f"/static/results/{result_filename}",
            reference_height=reference_height,
            unit=unit,
            pixel_ratio=pixel_ratio,
            horizontal_lines=h_lines,
            vertical_lines=v_lines,
            notes=notes,
            created_at=db_measurement.created_at,
            updated_at=db_measurement.updated_at,
        )

    except HTTPException:
        raise
    except ValueError as e:
        raise HTTPException(422, str(e))
    except Exception as e:
        raise HTTPException(500, f"Processing failed: {str(e)}")
