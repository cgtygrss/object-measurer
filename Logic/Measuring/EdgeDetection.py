import cv2
import numpy as np

import Data.Object as dataObj
import DrawGrid
from PIL import Image
import os


#Directory of Images
directory = "../../Images"

testImage = "../../Images/0.jpg"

def EdgeDetection(param_img):

    img = cv2.imread(param_img)
    # convert the image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    # Apply thresholding in the gray image to create a binary image
    ret, thresh = cv2.threshold(gray, 150, 255, 0)


    # Find the contours using binary image
    contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    print("Number of contours in image:", len(contours))


    for cnt in contours:
        # if the contour is not sufficiently large, ignore it
        if cv2.contourArea(cnt) < 10000:
            continue
        cv2.polylines(img, [cnt], True, (255, 0, 0), 2)
        (x, y), (w, h), angle = cv2.minAreaRect(cnt)
        print(x, y)
        print(w, h)
        print(angle)

    img_pil = Image.fromarray(img)
    DrawGrid.DrawGrid(img_pil)


EdgeDetection(testImage)


# for image in os.listdir(directory):
#     EdgeDetection(image)
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()

