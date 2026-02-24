import os
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import FileResponse
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database.db import get_db
from app.models.measurement import (
    MeasurementDB,
    MeasurementResult,
    MeasurementSummary,
    MeasurementUpdate,
    MeasurementLine,
)

router = APIRouter(prefix="/api/history", tags=["History"])


@router.get("/", response_model=List[MeasurementSummary])
async def list_measurements(
    skip: int = Query(0, ge=0),
    limit: int = Query(20, ge=1, le=100),
    db: AsyncSession = Depends(get_db),
):
    """List all measurements with pagination."""
    result = await db.execute(
        select(MeasurementDB)
        .order_by(desc(MeasurementDB.created_at))
        .offset(skip)
        .limit(limit)
    )
    measurements = result.scalars().all()

    return [
        MeasurementSummary(
            id=m.id,
            title=m.title,
            result_image_url=f"/static/results/{m.result_image_path}" if m.result_image_path else None,
            reference_height=m.reference_height,
            unit=m.unit,
            created_at=m.created_at,
        )
        for m in measurements
    ]


@router.get("/{measurement_id}", response_model=MeasurementResult)
async def get_measurement(
    measurement_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Get a specific measurement with all details."""
    result = await db.execute(
        select(MeasurementDB).where(MeasurementDB.id == measurement_id)
    )
    m = result.scalar_one_or_none()

    if not m:
        raise HTTPException(404, "Measurement not found")

    h_lines = [MeasurementLine(**l) for l in (m.horizontal_measurements or [])]
    v_lines = [MeasurementLine(**l) for l in (m.vertical_measurements or [])]

    return MeasurementResult(
        id=m.id,
        title=m.title,
        original_image_url=f"/static/uploads/{m.original_image_path}",
        result_image_url=f"/static/results/{m.result_image_path}" if m.result_image_path else None,
        reference_height=m.reference_height,
        unit=m.unit,
        pixel_ratio=m.pixel_ratio,
        horizontal_lines=h_lines,
        vertical_lines=v_lines,
        notes=m.notes,
        created_at=m.created_at,
        updated_at=m.updated_at,
    )


@router.patch("/{measurement_id}", response_model=MeasurementSummary)
async def update_measurement(
    measurement_id: int,
    update: MeasurementUpdate,
    db: AsyncSession = Depends(get_db),
):
    """Update measurement title or notes."""
    result = await db.execute(
        select(MeasurementDB).where(MeasurementDB.id == measurement_id)
    )
    m = result.scalar_one_or_none()

    if not m:
        raise HTTPException(404, "Measurement not found")

    if update.title is not None:
        m.title = update.title
    if update.notes is not None:
        m.notes = update.notes

    await db.flush()
    await db.refresh(m)

    return MeasurementSummary(
        id=m.id,
        title=m.title,
        result_image_url=f"/static/results/{m.result_image_path}" if m.result_image_path else None,
        reference_height=m.reference_height,
        unit=m.unit,
        created_at=m.created_at,
    )


@router.delete("/{measurement_id}")
async def delete_measurement(
    measurement_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Delete a measurement and its associated files."""
    result = await db.execute(
        select(MeasurementDB).where(MeasurementDB.id == measurement_id)
    )
    m = result.scalar_one_or_none()

    if not m:
        raise HTTPException(404, "Measurement not found")

    # Clean up files
    for path in [
        os.path.join(settings.UPLOAD_DIR, m.original_image_path),
        os.path.join(settings.RESULTS_DIR, m.result_image_path) if m.result_image_path else None,
    ]:
        if path and os.path.exists(path):
            os.remove(path)

    await db.delete(m)
    return {"message": "Measurement deleted successfully"}
