import numpy as np
from PIL import Image
import cv2

testImage = "../../RefinedImages/newimage.jpg"


def get_image(image_path):
    """Get a numpy array of an image so that one can access values[x][y]."""
    _image = Image.open(image_path, "r")
    width, height = _image.size
    pixel_values = list(_image.getdata())
    if _image.mode == "RGB":
        channels = 3
    elif _image.mode == "L":
        channels = 1
    else:
        print("Unknown mode: %s" % _image.mode)
        return None
    pixel_values = np.array(pixel_values).reshape((width, height, channels))
    return pixel_values


image = get_image(testImage)

reddish_pixels = [
    [200, 0, 1],
    [223, 22, 28],
    [196, 54, 42],
    [163, 52, 32],
    [150, 43, 61],
    [179, 44, 61],
    [238, 34, 45],
    [185, 0, 0]
]

np_rp = np.asarray(reddish_pixels)

img = cv2.imread(testImage)
_width, _height = img.shape[:2]
#
# for y in range(_height):
#     results = []
#     for x in range(_width):
#         for i in range(0, 8):
#             if image[y][x][0] == np_rp[i][0] and image[y][x][1] == np_rp[i][1] and image[y][x][2] == np_rp[i][2]:
#                 cv2.circle(img, (y, x), 2, (255, 0, 0), -1)
#                 print(f"{y} {x}")

# print(image)
# print(np_rp)

# print(img[125, 43])
# cv2.circle(img, (43, 125), 2, (255, 0, 0), -1)
# img[125, 43] = (255, 0, 0)
cv2.imshow("test", img)
cv2.waitKey(0)

# print(img[125, 43])

# print(_height, _width)
