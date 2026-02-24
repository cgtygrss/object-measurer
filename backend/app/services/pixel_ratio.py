from typing import List
from app.services.intersection import unpack_contours, get_distinct_x_intersections


def calculate_pixel_ratio(
    contour_list: list, interval: int, known_height: float
) -> float:
    """
    Calculate the pixel-to-real-world ratio using a known height.

    Args:
        contour_list: OpenCV contours
        interval: Grid interval in pixels
        known_height: Known real-world height of reference object

    Returns:
        Ratio: real_world_units per pixel
    """
    coords = unpack_contours(contour_list)
    distinct_x = get_distinct_x_intersections(coords, interval)

    if len(distinct_x) < 2:
        raise ValueError("Cannot determine pixel ratio: not enough intersection points")

    min_y = min(distinct_x)
    max_y = max(distinct_x)
    pixel_height = max_y - min_y

    if pixel_height == 0:
        raise ValueError("Cannot determine pixel ratio: zero pixel height")

    return known_height / pixel_height
