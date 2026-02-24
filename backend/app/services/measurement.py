import cv2
import numpy as np
import random
from typing import List, Dict, Tuple
from PIL import Image

from app.models.measurement import MeasurementLine, MeasurementPoint


def _random_color() -> Tuple[int, int, int]:
    return (random.randint(50, 200), random.randint(50, 200), random.randint(50, 200))


def draw_and_collect_horizontal(
    img: np.ndarray,
    y_coords: List[List[List[int]]],
    pixel_ratio: float,
    unit: str,
    min_distance: int = 25,
) -> List[MeasurementLine]:
    """Draw horizontal measurement lines and return measurement data."""
    lines = []
    y_coords_sorted = sorted(y_coords, key=lambda k: k[0] if k else [0])

    for group in y_coords_sorted:
        group.sort()
        for i in range(len(group) - 1):
            p1, p2 = group[i], group[i + 1]
            if p2[1] - p1[1] >= min_distance:
                color = _random_color()
                distance = (p2[1] - p1[1]) * pixel_ratio

                cv2.line(img, tuple(p1), tuple(p2), color, 2)
                label = f"{distance:.1f}{unit}"
                cv2.putText(
                    img, label, tuple(p1),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 0, 0), 1,
                    cv2.LINE_AA,
                )

                lines.append(MeasurementLine(
                    start=MeasurementPoint(x=p1[0], y=p1[1]),
                    end=MeasurementPoint(x=p2[0], y=p2[1]),
                    distance=round(distance, 2),
                    unit=unit,
                ))
    return lines


def draw_and_collect_vertical(
    img: np.ndarray,
    x_coords: List[List[List[int]]],
    pixel_ratio: float,
    unit: str,
    min_distance: int = 25,
) -> List[MeasurementLine]:
    """Draw vertical measurement lines and return measurement data."""
    lines = []
    x_coords_sorted = sorted(x_coords, key=lambda k: k[0] if k else [0])

    for group in x_coords_sorted:
        group.sort()
        for i in range(len(group) - 1):
            p1, p2 = group[i], group[i + 1]
            if p2[0] - p1[0] >= min_distance:
                color = _random_color()
                distance = (p2[0] - p1[0]) * pixel_ratio

                cv2.line(img, tuple(p1), tuple(p2), color, 2)
                label = f"{distance:.1f}{unit}"
                cv2.putText(
                    img, label, (p2[0] + 10, p2[1]),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1,
                    cv2.LINE_AA,
                )

                lines.append(MeasurementLine(
                    start=MeasurementPoint(x=p1[0], y=p1[1]),
                    end=MeasurementPoint(x=p2[0], y=p2[1]),
                    distance=round(distance, 2),
                    unit=unit,
                ))
    return lines


def measure_object(
    img: np.ndarray,
    horizontal_intersections: List[List[List[int]]],
    vertical_intersections: List[List[List[int]]],
    pixel_ratio: float,
    unit: str = "cm",
) -> Tuple[Image.Image, List[MeasurementLine], List[MeasurementLine]]:
    """
    Measure an object by drawing dimension lines on the image.

    Returns:
        Tuple of (annotated PIL Image, horizontal lines, vertical lines)
    """
    h_lines = draw_and_collect_horizontal(img, horizontal_intersections, pixel_ratio, unit)
    v_lines = draw_and_collect_vertical(img, vertical_intersections, pixel_ratio, unit)

    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img_rgb)

    return img_pil, h_lines, v_lines
