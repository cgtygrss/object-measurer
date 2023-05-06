import cv2
import os
from PIL import Image
from Logic.ImageOperations.ImageOperations import *
import asyncio


async def save_image(image, image_name, path):
    img_cv2 = convert_image_to_cv2(image)
    cv2.imwrite(f"{path}/{image_name}", img_cv2)
