import cv2
from Logic.Utils.ConvertUtil import convert_image_to_cv2


def save_image(image, image_name, path):
    img_cv2 = convert_image_to_cv2(image)
    cv2.imwrite(f"{path}/{image_name}", img_cv2)
