import cv2
import numpy as np


def edge_detection(param_img):
    try:
        img = param_img

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        ret, thresh = cv2.threshold(gray, 210, 255, cv2.THRESH_BINARY)
        thresh = 255 - thresh

        shapes, hierarchy = cv2.findContours(image=thresh, mode=cv2.RETR_EXTERNAL, method=cv2.CHAIN_APPROX_NONE)
        cv2.drawContours(image=img, contours=shapes, contourIdx=-1, color=(0, 255, 0), thickness=2,
                         lineType=cv2.LINE_AA)

        print("Number of contours in image:", len(shapes))

        contours_list = []

        for cnt in shapes:
            for item in cnt:
                contours_list.append(item)

        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        return img, list(shapes)

    except Exception as e:
        print(e)
