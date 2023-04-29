import cv2
from Logic.Grid import DrawGrid
from PIL import Image
from Logic.SpecifyIntersections import SpecifyIntersections
from Logic.SaveFile import SaveFile


def edge_detection(param_img):
    try:
        img = cv2.imread(param_img)
        # convert the image to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

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
            cv2.drawContours(img, [cnt], 0, (0, 255, 0), 2)

        return img, contours_list

    except Exception as e:
        print(e)
