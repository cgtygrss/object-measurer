import os
import sys
import numpy
from Logic.CameraOperations.OpenCamera import open_camera
from Logic.ImageOperations.EdgeDetection import edge_detection
from Logic.ImageOperations.MeasureObject import calculate_object_height_pixel_ratio
from Logic.ImageOperations.MeasureObject import measure
from Logic.ImageOperations.RemoveBackground import remove_background
from Logic.ImageOperations.SpecifyIntersections import find_intersections
from Logic.SaveFile.SaveFile import save_image

numpy.set_printoptions(threshold=sys.maxsize)

# Directory of Images
first_path = "Images"

# Directory of RefinedImages
path = "RefinedImages"

# How much pixel blanks will be given after one grid.
interval = 20

# The list we had to keep Images in it.
image_directory_list = []


def main():
    # open camera and take photos
    open_camera(first_path)

    height = int(input("Enter object Height : "))
    pixel_ratio = 0

    for file in os.listdir("Images"):
        image_directory_list.append("Images/" + file)

    for item in image_directory_list:

        try:
            # Remove background of the image
            img = remove_background(item)

            # Apply edge detection to image and find contours
            img_cv2, contour_list = edge_detection(img)

            # Find intersection points of grid and image
            horizontal_list, vertical_list = find_intersections(contour_list, interval)

            if item == "Images/0.jpg":
                pixel_ratio = calculate_object_height_pixel_ratio(vertical_list, height)

            # Measure object and save final image.
            # Takes Image,ImageName,Image Saving Path, Horizontal Intersection List, Vertical Intersection List
            final_image = measure(img_cv2, horizontal_list, vertical_list, pixel_ratio)

            save_image(final_image, item[7:], path)

        except Exception as ex:
            print(ex)


main()
