import cv2
import numpy as np

testImage = "../../Images/0.jpg"


def shadow_remove(img, img_bg):

    # Visualization
    scale_percent = 40  # percent of original size
    width = int(img.shape[1] * scale_percent / 100)
    height = int(img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    img = cv2.resize(img, dim, interpolation=cv2.INTER_AREA)
    img_bg = cv2.resize(img_bg, dim, interpolation=cv2.INTER_AREA)
    rgb_planes = cv2.split(img)

    result_norm_planes = []
    for plane in rgb_planes:
        dilated_img = cv2.dilate(plane, np.ones((7, 7), np.uint8))
        bg_img = cv2.medianBlur(dilated_img, 21)
        diff_img = 255 - cv2.absdiff(plane, bg_img)
        norm_img = cv2.normalize(diff_img, None, alpha=0, beta=255, norm_type=cv2.NORM_MINMAX, dtype=cv2.CV_8UC1)
        result_norm_planes.append(norm_img)

    removed = cv2.merge(result_norm_planes)

    return removed
