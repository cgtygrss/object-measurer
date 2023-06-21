import numpy as np
from rembg import remove
from PIL import Image


def convert_image_to_cv2(param_image):
    open_cv_image = np.array(param_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image


def remove_background(param_img):
    im = Image.open(param_img)
    output = remove(im, bgcolor=(255, 255, 255, 255)).convert('RGB')
    converted_image = convert_image_to_cv2(output)

    return converted_image
