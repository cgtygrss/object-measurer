import cv2
import numpy as np

testImage = "../../Images/Screenshot_1.png"


# load the image, convert it to grayscale, and blur it slightly
img = cv2.imread(testImage)
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# blurred = cv2.GaussianBlur(gray, (3, 3), 0)

blurred_img = cv2.blur(img,ksize=(5,5))
med_val = np.median(img)
lower = int(max(0 ,0.7*med_val))
upper = int(min(255,1.3*med_val))
edges = cv2.Canny(image=img, threshold1=lower,threshold2=upper)

# show the images
cv2.imshow("Original", img)
cv2.imshow("test", edges)
# cv2.imshow("Edges", np.hstack([wide, tight, auto]))
cv2.waitKey(0)
