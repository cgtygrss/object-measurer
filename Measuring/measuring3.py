import cv2
import numpy as np

# Load the image
img = cv2.imread('../Images/test.jpg')

# Set the known distance between the two points in meters
known_distance = 1.0

# Set the known width of the object in meters
known_width = 0.5

# Set the focal length of the camera in pixels
focal_length = 500

# Identify the two points on the object
point1 = (100, 100)
point2 = (200, 100)

# Calculate the distance between the two points in pixels
pixel_distance = np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Calculate the angular size of the object
angular_size = 2 * np.arctan(known_width / (2 * focal_length))

# Calculate the distance to the object in meters
distance = known_distance / np.tan(angular_size / 2)

# Draw a line between the two points on the object
cv2.line(img, point1, point2, (0, 255, 0), 2)

# Display the distance on the image
cv2.putText(img, "{:.2f}m".format(distance), (int((point1[0]+point2[0])/2), int((point1[1]+point2[1])/2)), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

# Display the image
cv2.imshow('image', img)
cv2.waitKey(0)
cv2.destroyAllWindows()