import cv2
import numpy as np


def canny(param_img):
    med_val = np.median(param_img)
    lower = int(max(0, 0.5 * med_val))
    upper = int(min(255, 1.3 * med_val))
    gray = cv2.cvtColor(param_img, cv2.COLOR_BGR2GRAY)
    edges = cv2.Canny(image=gray, threshold1=lower, threshold2=upper)

    return edges
