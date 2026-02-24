import numpy as np
from rembg import remove
from PIL import Image
from io import BytesIO


def remove_background(image_bytes: bytes) -> np.ndarray:
    """Remove background from image bytes and return CV2-compatible numpy array."""
    im = Image.open(BytesIO(image_bytes))
    output = remove(im, bgcolor=(255, 255, 255, 255)).convert("RGB")
    cv2_image = np.array(output)[:, :, ::-1].copy()  # RGB → BGR
    return cv2_image


def remove_background_to_pil(image_bytes: bytes) -> Image.Image:
    """Remove background and return PIL Image."""
    im = Image.open(BytesIO(image_bytes))
    output = remove(im, bgcolor=(255, 255, 255, 255)).convert("RGB")
    return output
