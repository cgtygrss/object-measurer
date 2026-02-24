import os
from io import BytesIO
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import StreamingResponse
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import cm
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image as RLImage, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

from app.config import settings
from app.database.db import get_db
from app.models.measurement import MeasurementDB

router = APIRouter(prefix="/api/export", tags=["Export"])


@router.get("/{measurement_id}/pdf")
async def export_measurement_pdf(
    measurement_id: int,
    db: AsyncSession = Depends(get_db),
):
    """Export a measurement as a PDF report."""
    result = await db.execute(
        select(MeasurementDB).where(MeasurementDB.id == measurement_id)
    )
    m = result.scalar_one_or_none()

    if not m:
        raise HTTPException(404, "Measurement not found")

    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=1.5 * cm, bottomMargin=1.5 * cm)
    styles = getSampleStyleSheet()
    story = []

    # Title
    title_style = ParagraphStyle(
        "CustomTitle", parent=styles["Title"], fontSize=24, spaceAfter=12
    )
    story.append(Paragraph(f"Measurement Report: {m.title}", title_style))
    story.append(Spacer(1, 12))

    # Metadata table
    meta_data = [
        ["Reference Height", f"{m.reference_height} {m.unit}"],
        ["Pixel Ratio", f"{m.pixel_ratio:.6f}" if m.pixel_ratio else "N/A"],
        ["Date", m.created_at.strftime("%Y-%m-%d %H:%M")],
    ]
    if m.notes:
        meta_data.append(["Notes", m.notes])

    meta_table = Table(meta_data, colWidths=[4 * cm, 12 * cm])
    meta_table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.Color(0.9, 0.9, 0.9)),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("PADDING", (0, 0), (-1, -1), 8),
        ("FONTNAME", (0, 0), (0, -1), "Helvetica-Bold"),
    ]))
    story.append(meta_table)
    story.append(Spacer(1, 20))

    # Result image
    if m.result_image_path:
        img_path = os.path.join(settings.RESULTS_DIR, m.result_image_path)
        if os.path.exists(img_path):
            story.append(Paragraph("Measured Image", styles["Heading2"]))
            img = RLImage(img_path, width=16 * cm, height=12 * cm, kind="proportional")
            story.append(img)
            story.append(Spacer(1, 16))

    # Horizontal measurements
    h_measurements = m.horizontal_measurements or []
    if h_measurements:
        story.append(Paragraph("Horizontal Measurements", styles["Heading2"]))
        h_data = [["#", "Start", "End", f"Distance ({m.unit})"]]
        for i, line in enumerate(h_measurements, 1):
            start = line.get("start", {})
            end = line.get("end", {})
            h_data.append([
                str(i),
                f"({start.get('x', 0)}, {start.get('y', 0)})",
                f"({end.get('x', 0)}, {end.get('y', 0)})",
                f"{line.get('distance', 0):.2f}",
            ])
        h_table = Table(h_data, colWidths=[1.5 * cm, 4 * cm, 4 * cm, 4 * cm])
        h_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.4, 0.8)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))
        story.append(h_table)
        story.append(Spacer(1, 16))

    # Vertical measurements
    v_measurements = m.vertical_measurements or []
    if v_measurements:
        story.append(Paragraph("Vertical Measurements", styles["Heading2"]))
        v_data = [["#", "Start", "End", f"Distance ({m.unit})"]]
        for i, line in enumerate(v_measurements, 1):
            start = line.get("start", {})
            end = line.get("end", {})
            v_data.append([
                str(i),
                f"({start.get('x', 0)}, {start.get('y', 0)})",
                f"({end.get('x', 0)}, {end.get('y', 0)})",
                f"{line.get('distance', 0):.2f}",
            ])
        v_table = Table(v_data, colWidths=[1.5 * cm, 4 * cm, 4 * cm, 4 * cm])
        v_table.setStyle(TableStyle([
            ("BACKGROUND", (0, 0), (-1, 0), colors.Color(0.2, 0.7, 0.3)),
            ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
            ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
            ("PADDING", (0, 0), (-1, -1), 6),
            ("FONTNAME", (0, 0), (-1, 0), "Helvetica-Bold"),
            ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.Color(0.95, 0.95, 0.95)]),
        ]))
        story.append(v_table)

    doc.build(story)
    buffer.seek(0)

    return StreamingResponse(
        buffer,
        media_type="application/pdf",
        headers={
            "Content-Disposition": f'attachment; filename="measurement_{m.id}_{m.title}.pdf"'
        },
    )
