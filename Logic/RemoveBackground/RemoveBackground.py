from rembg import remove
from PIL import Image


def remove_background(param_img):
    im = Image.open(param_img)
    output = remove(im, bgcolor=(255, 255, 255, 255)).convert('RGB')

    return output
