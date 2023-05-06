import cv2
import numpy as np


def edge_detection(param_img):
    try:
        # convert the image to grayscale
        gray = cv2.cvtColor(param_img, cv2.COLOR_BGR2GRAY)

        # Apply thresholding in the gray image to create a binary image
        ret, thresh = cv2.threshold(gray, 150, 255, 0)

        # Find the contours using binary image
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)

        print("Number of contours in image:", len(contours))

        contours_list = []

        for cnt in contours:
            # if the contour is not sufficiently large, ignore it
            if cv2.contourArea(cnt) < 10000:
                continue
            # remove if the contour is too large
            elif cv2.contourArea(cnt) > 1000000:
                continue
            contours_list.append(cnt)
            cv2.drawContours(param_img, [cnt], 0, (0, 255, 0), 2)

        return param_img, contours_list

    except Exception as e:
        print(e)
