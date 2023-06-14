import numpy as np
from rembg import remove
from PIL import Image
import cv2


def convert_image_to_cv2(param_image):
    open_cv_image = np.array(param_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image


def remove_background(param_img):
    im = Image.open(param_img)
    output = remove(im, bgcolor=(255, 255, 255, 255)).convert('RGB')
    output.save("test.png")

    return output


def resize_image(param_img, scale_percent):
    # Visualization
    width = int(param_img.shape[1] * scale_percent / 100)
    height = int(param_img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    img = cv2.resize(param_img, dim, interpolation=cv2.INTER_AREA)

    return img