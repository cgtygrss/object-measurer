from scipy.spatial import distance as dist
from imutils import perspective
from imutils import contours
import numpy as np
import argparse
import imutils
import cv2


def midpoint(pointA, pointB):
	return ((pointA[0] + pointB[0]) * 0.5, (pointA[1] + pointB[1]) * 0.5)


ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="testingImage.jpg")

#ap.add_argument("-w", "--width", type=float, required=True, help="width of the left-most object in the image (in inches)") ?

args = vars(ap.parse_args())

# load the image, convert it to grayscale, and blur it slightly
image = cv2.imread(args["testingImage.jpg"])
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (7, 7), 0)


edged = cv2.Canny(gray, 50, 100)
edged = cv2.dilate(edged, None, iterations=1)
edged = cv2.erode(edged, None, iterations=1)


cnts = cv2.findContours(edged.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
cnts = imutils.grab_contours(cnts)


(cnts, _) = contours.sort_contours(cnts)
pixelsPerMetric = None
