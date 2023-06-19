import cv2

from Logic.Grid.DrawGrid import *
from Logic.Detecting.EdgeDetection import *
from Logic.Detecting.Canny import *
from Logic.SpecifyIntersections.SpecifyIntersections import *
from Logic.Measuring.MeasureObject import *
from Logic.ImageOperations.ImageOperations import *
from Logic.CameraOperations.Camera.OpenCamera import *
from Data import *
import sys
import numpy

numpy.set_printoptions(threshold=sys.maxsize)

# Directory of Images
first_path = "Images"

# Directory of RefinedImages
path = "RefinedImages"

# How much pixel blanks will be given after one grid.
grid_interval = 20

# At what percentage will the image be resized?
scale_percent = 40


# The list we had to keep Images in it.
image_directory_list = []


async def main():
    # open camera and take photos
    await open_camera(first_path)

    for file in os.listdir("Images"):
        image_directory_list.append("Images/" + file)

    for item in image_directory_list:

        try:
            # Remove background of the image
            img = remove_background(item)

            # Convert PIL Image to CV2
            converted_img = convert_image_to_cv2(img)

            # Resize image
            resized_img = resize_image(converted_img, scale_percent)

            # Apply edge detection to image and find contours
            img_cv2, contour_list = edge_detection(resized_img)

            # Draw grid on detected image
            grid_img = draw_grid(img_cv2, grid_interval)

            # Find intersection points of grid and image
            horizontal_list, vertical_list = find_intersection(contour_list, grid_interval)

            if item == "Images/0.jpg":
                pixel_ratio = calculate_object_height_pixel_ratio(horizontal_list, height)

            # print(contour_list)
            # Measure object and save final image.
            # Takes Image,ImageName,Image Saving Path, Horizontal Intersection List, Vertical Intersection List
            final_image = measure(grid_img, horizontal_list, vertical_list)

            await save_image(final_image, item[7:], path)

        except Exception as ex:
            print(ex)


asyncio.run(main())
