import os

from Logic.Grid.DrawGrid import *
from Logic.Detecting.EdgeDetection import *
from Logic.SpecifyIntersections.SpecifyIntersections import *
from Logic.Measuring.MeasureObject import *

# Directory of RefinedImages
path = "RefinedImages"

image_directory_list = []


for file in os.listdir("Images"):
    image_directory_list.append("Images/" + file)


for item in image_directory_list:

    try:
        # Apply edge detection to image and find contours
        img_cv2, contour_list = edge_detection(item)

        # Draw grid on detected image
        grid_img = draw_grid(img_cv2)

        # Find intersection points of gid and image
        horizontal_list, vertical_list = find_intersection(contour_list)

        # Measure object and save final image.
        # Takes Image,ImageName,Image Saving Path, Horizontal Intersection List, Vertical Intersection List
        measure_and_save(grid_img, item[7:], path, horizontal_list, vertical_list)
    except Exception as ex:
        print(ex)
