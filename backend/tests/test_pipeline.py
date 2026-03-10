"""Tests for measurement pipeline — accuracy and correctness."""

import os
import pytest
from app.measurement.pipeline import (
    load_image_from_bytes,
    remove_background,
    detect_edges,
    calculate_pixel_ratio,
    find_intersections,
    measure_and_annotate,
    run_measurement_pipeline,
    image_to_base64,
)

# Path to original test images from the university project
IMAGES_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "Images")


def get_test_image_bytes(filename: str) -> bytes:
    """Load a test image from the Images directory."""
    path = os.path.join(IMAGES_DIR, filename)
    if not os.path.exists(path):
        pytest.skip(f"Test image not found: {path}")
    with open(path, "rb") as f:
        return f.read()


class TestImageLoading:
    def test_load_valid_image(self):
        """Test loading a valid image from bytes."""
        img_bytes = get_test_image_bytes("0.jpg")
        img = load_image_from_bytes(img_bytes)
        assert img is not None
        assert img.shape[2] == 3  # BGR channels
        assert img.shape[0] > 0
        assert img.shape[1] > 0

    def test_load_invalid_bytes(self):
        """Test loading invalid bytes raises ValueError."""
        with pytest.raises(ValueError, match="Could not decode"):
            load_image_from_bytes(b"not an image")


class TestBackgroundRemoval:
    def test_remove_background(self):
        """Test background removal produces valid output."""
        img_bytes = get_test_image_bytes("0.jpg")
        img = load_image_from_bytes(img_bytes)
        result = remove_background(img)
        assert result is not None
        assert result.shape == img.shape  # Same dimensions


class TestEdgeDetection:
    def test_detect_edges(self):
        """Test edge detection finds contours."""
        img_bytes = get_test_image_bytes("0.jpg")
        img = load_image_from_bytes(img_bytes)
        clean = remove_background(img)
        img_edges, contours = detect_edges(clean)

        assert img_edges is not None
        assert len(contours) > 0
        print(f"Found {len(contours)} contours")


class TestPixelRatio:
    def test_calculate_ratio(self):
        """Test pixel ratio calculation with known reference."""
        img_bytes = get_test_image_bytes("0.jpg")
        img = load_image_from_bytes(img_bytes)
        clean = remove_background(img)
        _, contours = detect_edges(clean)

        if not contours:
            pytest.skip("No contours found")

        ratio = calculate_pixel_ratio(contours, interval=20, reference_height_mm=100)
        assert ratio > 0
        print(f"Pixel ratio: {ratio}")


class TestIntersections:
    def test_find_intersections(self):
        """Test intersection finding returns valid results."""
        img_bytes = get_test_image_bytes("0.jpg")
        img = load_image_from_bytes(img_bytes)
        clean = remove_background(img)
        _, contours = detect_edges(clean)

        if not contours:
            pytest.skip("No contours found")

        h_list, v_list = find_intersections(contours, interval=20)
        assert isinstance(h_list, list)
        assert isinstance(v_list, list)
        print(f"Horizontal groups: {len(h_list)}, Vertical groups: {len(v_list)}")


class TestFullPipeline:
    def test_run_pipeline(self):
        """Test full measurement pipeline end-to-end."""
        img_bytes = get_test_image_bytes("0.jpg")

        result = run_measurement_pipeline(
            image_bytes=img_bytes,
            reference_height_mm=100,
            interval=20,
        )

        assert result.contour_count > 0
        assert result.pixel_ratio > 0
        assert result.width_mm > 0
        assert result.height_mm > 0
        assert result.area_mm2 > 0
        assert result.annotated_image is not None

        print(f"Width: {result.width_mm}mm")
        print(f"Height: {result.height_mm}mm")
        print(f"Area: {result.area_mm2}mm²")
        print(f"Contours: {result.contour_count}")
        print(f"H distances: {result.horizontal_distances[:5]}")
        print(f"V distances: {result.vertical_distances[:5]}")

    def test_run_pipeline_all_images(self):
        """Test pipeline works on all sample images."""
        for filename in ["0.jpg", "90.jpg"]:
            img_bytes = get_test_image_bytes(filename)
            result = run_measurement_pipeline(
                image_bytes=img_bytes,
                reference_height_mm=100,
                interval=20,
            )
            assert result.contour_count > 0, f"No contours found in {filename}"
            print(f"{filename}: {result.width_mm}x{result.height_mm}mm, {result.contour_count} contours")


class TestImageEncoding:
    def test_base64_encoding(self):
        """Test image-to-base64 encoding."""
        img_bytes = get_test_image_bytes("0.jpg")
        img = load_image_from_bytes(img_bytes)
        b64 = image_to_base64(img)
        assert len(b64) > 0
        assert isinstance(b64, str)
