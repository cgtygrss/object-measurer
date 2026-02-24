import cv2
import numpy as np
from typing import List, Tuple


def detect_edges(image: np.ndarray) -> Tuple[np.ndarray, List[np.ndarray]]:
    """
    Apply edge detection to an image.

    Args:
        image: BGR numpy array

    Returns:
        Tuple of (annotated image, list of contours)
    """
    img = image.copy()
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    ret, thresh = cv2.threshold(blurred, 240, 255, cv2.THRESH_BINARY)
    thresh = 255 - thresh

    # Morphological operations to clean up
    kernel = np.ones((3, 3), np.uint8)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel, iterations=2)
    thresh = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)

    contours, hierarchy = cv2.findContours(
        image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE
    )

    # Filter out small noise contours
    min_area = 500
    filtered_contours = [c for c in contours if cv2.contourArea(c) > min_area]

    cv2.drawContours(
        image=img,
        contours=filtered_contours,
        contourIdx=-1,
        color=(0, 255, 0),
        thickness=2,
        lineType=cv2.LINE_AA,
    )

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    return img, list(filtered_contours)


def get_bounding_box(contours: List[np.ndarray]) -> Tuple[int, int, int, int]:
    """Get bounding box encompassing all contours."""
    if not contours:
        return (0, 0, 0, 0)

    all_points = np.vstack(contours)
    x, y, w, h = cv2.boundingRect(all_points)
    return (x, y, w, h)
