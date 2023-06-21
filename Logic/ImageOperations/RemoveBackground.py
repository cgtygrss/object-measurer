import numpy as np
from rembg import remove
from PIL import Image
from Logic.Utils.ConvertUtil import convert_image_to_cv2


def remove_background(param_img):
    im = Image.open(param_img)
    output = remove(im, bgcolor=(255, 255, 255, 255)).convert('RGB')
    converted_image = convert_image_to_cv2(output)

    return converted_image
