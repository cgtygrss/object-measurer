from Logic.Grid.DrawGrid import *
from Logic.Detecting.EdgeDetection import *
from Logic.Detecting.Canny import *
from Logic.SpecifyIntersections.SpecifyIntersections import *
from Logic.Measuring.MeasureObject import *
from Logic.ImageOperations.ImageOperations import *

# Directory of RefinedImages
path = "RefinedImages"

# How much pixel blanks will be given after one grid.
grid_interval = 5

# At what percentage will the image be resized?
scale_percent = 60

# The list we had to keep Images in it.
image_directory_list = []


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

        # Apply canny edge detection
        canny_img = canny(resized_img)

        # Apply edge detection to image and find contours
        img_cv2, contour_list = edge_detection(canny_img)

        # Draw grid on detected image
        grid_img = draw_grid(img_cv2, grid_interval)

        # Find intersection points of grid and image
        horizontal_list, vertical_list = find_intersection(contour_list, grid_interval)

        # Measure object and save final image.
        # Takes Image,ImageName,Image Saving Path, Horizontal Intersection List, Vertical Intersection List
        measure_and_save(grid_img, item[7:], path, horizontal_list, vertical_list)

    except Exception as ex:
        print(ex)
