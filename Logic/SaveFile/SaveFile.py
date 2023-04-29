import cv2
import os
from PIL import Image


def save_image(image, image_name, path):
   image.save(f"{path}/{image_name}")
