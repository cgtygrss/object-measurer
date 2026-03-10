"""
OpenCV measurement pipeline — ported from the original university project.

Original modules:
  - Logic/ImageOperations/RemoveBackground.py
  - Logic/ImageOperations/EdgeDetection.py
  - Logic/ImageOperations/PixelRatio.py
  - Logic/ImageOperations/SpecifyIntersections.py
  - Logic/ImageOperations/MeasureObject.py

Refactored to:
  - Accept raw image bytes instead of file paths
  - Return structured data (dicts) instead of saving files
  - Work as pure functions suitable for an API context
"""

import base64
import io
from dataclasses import dataclass, field

import cv2
import numpy as np
from PIL import Image
from rembg import remove


# ─── Data Structures ──────────────────────────────────────────

@dataclass
class MeasurementResult:
    """Structured result from the measurement pipeline."""
    width_mm: float = 0.0
    height_mm: float = 0.0
    area_mm2: float = 0.0
    contour_count: int = 0
    horizontal_distances: list[float] = field(default_factory=list)
    vertical_distances: list[float] = field(default_factory=list)
    annotated_image: np.ndarray | None = None
    pixel_ratio: float = 0.0


# ─── Pipeline Functions ───────────────────────────────────────

def load_image_from_bytes(image_bytes: bytes) -> np.ndarray:
    """Load an image from raw bytes into OpenCV format (BGR)."""
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    if img is None:
        raise ValueError("Could not decode image from provided bytes")
    return img


def remove_background(img: np.ndarray) -> np.ndarray:
    """
    Remove background from image, replacing it with white.
    Ported from: Logic/ImageOperations/RemoveBackground.py
    """
    # Convert OpenCV (BGR) to PIL
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)

    # Remove background with white fill
    output = remove(pil_img, bgcolor=(255, 255, 255, 255)).convert("RGB")

    # Convert back to OpenCV (BGR)
    result = cv2.cvtColor(np.array(output), cv2.COLOR_RGB2BGR)
    return result


def detect_edges(img: np.ndarray) -> tuple[np.ndarray, list]:
    """
    Apply edge detection and find contours.
    Ported from: Logic/ImageOperations/EdgeDetection.py
    """
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)
    thresh = 255 - thresh

    contours, _ = cv2.findContours(
        image=thresh, mode=cv2.RETR_TREE, method=cv2.CHAIN_APPROX_NONE
    )

    # Draw contours on the image
    img_with_contours = img.copy()
    cv2.drawContours(
        image=img_with_contours,
        contours=contours,
        contourIdx=-1,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA,
    )

    return img_with_contours, list(contours)


def _get_sub_lists(contour_list: list) -> list:
    """
    Convert contour arrays to nested coordinate lists.
    Ported from: Logic/Utils/ListUtil.py
    """
    coords = []
    for cnt in contour_list:
        sub = []
        for point in cnt:
            sub.append(point[0].tolist())
        coords.append(sub)
    return coords


def _get_distinct_x_intersections(coords: list, interval: int) -> list[int]:
    """Find distinct x-axis intersection points at grid intervals."""
    distinct = []
    for sublist in coords:
        for point in sublist:
            if point[1] not in distinct and point[1] % interval == 0:
                distinct.append(point[1])
    return distinct


def _get_distinct_y_intersections(coords: list, interval: int) -> list[int]:
    """Find distinct y-axis intersection points at grid intervals."""
    distinct = []
    for sublist in coords:
        for point in sublist:
            if point[0] not in distinct and point[0] % interval == 0:
                distinct.append(point[0])
    return distinct


def _get_horizontal_intersection_coords(coords: list, distinct_y: list) -> list:
    """Get coordinate pairs for horizontal measurement lines."""
    result = []
    for y_val in distinct_y:
        y_coords = []
        for sublist in coords:
            for point in sublist:
                if point not in y_coords and point[0] == y_val:
                    y_coords.append(point)
        result.append(y_coords)
    return result


def _get_vertical_intersection_coords(coords: list, distinct_x: list) -> list:
    """Get coordinate pairs for vertical measurement lines."""
    result = []
    for x_val in distinct_x:
        x_coords = []
        for sublist in coords:
            for point in sublist:
                if point not in x_coords and point[1] == x_val:
                    x_coords.append(point)
        result.append(x_coords)
    return result


def calculate_pixel_ratio(
    contour_list: list, interval: int, reference_height_mm: float
) -> float:
    """
    Calculate the pixel-to-mm ratio using a known reference object height.
    Ported from: Logic/ImageOperations/PixelRatio.py
    """
    coords = _get_sub_lists(contour_list)
    distinct_x = _get_distinct_x_intersections(coords, interval)

    if not distinct_x:
        raise ValueError("No intersection points found — cannot calculate pixel ratio")

    min_y = min(distinct_x)
    max_y = max(distinct_x)

    pixel_span = max_y - min_y
    if pixel_span == 0:
        raise ValueError("Zero pixel span — cannot calculate ratio")

    return reference_height_mm / pixel_span


def find_intersections(
    contour_list: list, interval: int
) -> tuple[list, list]:
    """
    Find horizontal and vertical intersection points between
    contour edges and a regular grid.
    Ported from: Logic/ImageOperations/SpecifyIntersections.py
    """
    coords = _get_sub_lists(contour_list)
    distinct_x = _get_distinct_x_intersections(coords, interval)
    distinct_y = _get_distinct_y_intersections(coords, interval)
    horizontal = _get_horizontal_intersection_coords(coords, distinct_y)
    vertical = _get_vertical_intersection_coords(coords, distinct_x)
    return horizontal, vertical


def measure_and_annotate(
    img: np.ndarray,
    horizontal_intersections: list,
    vertical_intersections: list,
    pixel_ratio: float,
) -> tuple[np.ndarray, list[float], list[float]]:
    """
    Draw measurement lines and annotate distances on the image.
    Ported from: Logic/ImageOperations/MeasureObject.py

    Returns:
        - Annotated image (BGR)
        - List of horizontal distances (mm)
        - List of vertical distances (mm)
    """
    h_distances = []
    v_distances = []

    # Horizontal measurements
    for y_coords in horizontal_intersections:
        y_coords.sort()
        for i in range(len(y_coords) - 1):
            p1 = y_coords[i]
            p2 = y_coords[i + 1]
            pixel_dist = p2[1] - p1[1]
            if pixel_dist >= 25:
                color = (
                    int(np.random.randint(0, 255)),
                    int(np.random.randint(0, 255)),
                    int(np.random.randint(0, 255)),
                )
                cv2.line(img, tuple(p1), tuple(p2), color, 2)
                distance_mm = round(pixel_dist * pixel_ratio, 2)
                h_distances.append(distance_mm)
                cv2.putText(
                    img,
                    f"{distance_mm}",
                    tuple(p1),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (255, 0, 0),
                )

    # Vertical measurements
    for x_coords in vertical_intersections:
        x_coords.sort()
        for i in range(len(x_coords) - 1):
            p1 = x_coords[i]
            p2 = x_coords[i + 1]
            pixel_dist = p2[0] - p1[0]
            if pixel_dist >= 25:
                color = (
                    int(np.random.randint(0, 255)),
                    int(np.random.randint(0, 255)),
                    int(np.random.randint(0, 255)),
                )
                cv2.line(img, tuple(p1), tuple(p2), color, 2)
                distance_mm = round(pixel_dist * pixel_ratio, 2)
                v_distances.append(distance_mm)
                cv2.putText(
                    img,
                    f"{distance_mm}",
                    (p2[0] + 20, p2[1]),
                    cv2.FONT_HERSHEY_COMPLEX,
                    0.5,
                    (0, 0, 0),
                )

    return img, h_distances, v_distances


def image_to_base64(img: np.ndarray, format: str = "JPEG") -> str:
    """Convert OpenCV image to base64 string for API response."""
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    pil_img = Image.fromarray(img_rgb)
    buffer = io.BytesIO()
    pil_img.save(buffer, format=format, quality=85)
    return base64.b64encode(buffer.getvalue()).decode("utf-8")


# ─── Main Pipeline ─────────────────────────────────────────────

def run_measurement_pipeline(
    image_bytes: bytes,
    reference_height_mm: float,
    interval: int = 20,
) -> MeasurementResult:
    """
    Run the full measurement pipeline on an uploaded image.

    Pipeline steps:
      1. Load image from bytes
      2. Remove background
      3. Detect edges and find contours
      4. Calculate pixel-to-mm ratio using reference height
      5. Find intersection points on a grid
      6. Measure distances and annotate the image

    Args:
        image_bytes: Raw image file content
        reference_height_mm: Known height of the reference object in mm
        interval: Grid interval in pixels (default: 20)

    Returns:
        MeasurementResult with dimensions and annotated image
    """
    # Step 1: Load image
    img = load_image_from_bytes(image_bytes)

    # Step 2: Remove background
    img_clean = remove_background(img)

    # Step 3: Edge detection
    img_edges, contours = detect_edges(img_clean)

    if not contours:
        return MeasurementResult(contour_count=0)

    # Step 4: Pixel ratio
    pixel_ratio = calculate_pixel_ratio(contours, interval, reference_height_mm)

    # Step 5: Find intersections
    horizontal, vertical = find_intersections(contours, interval)

    # Step 6: Measure and annotate
    annotated, h_distances, v_distances = measure_and_annotate(
        img_edges, horizontal, vertical, pixel_ratio
    )

    # Calculate overall dimensions from bounding rect of largest contour
    largest_contour = max(contours, key=cv2.contourArea)
    _, _, w_px, h_px = cv2.boundingRect(largest_contour)
    width_mm = round(w_px * pixel_ratio, 2)
    height_mm = round(h_px * pixel_ratio, 2)
    area_mm2 = round(width_mm * height_mm, 2)

    return MeasurementResult(
        width_mm=width_mm,
        height_mm=height_mm,
        area_mm2=area_mm2,
        contour_count=len(contours),
        horizontal_distances=h_distances,
        vertical_distances=v_distances,
        annotated_image=annotated,
        pixel_ratio=pixel_ratio,
    )
