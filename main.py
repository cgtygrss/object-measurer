from Logic.Grid.DrawGrid import *
from Logic.Detecting.EdgeDetection import *
from Logic.RemoveBackground.RemoveBackground import *
from Logic.SpecifyIntersections.SpecifyIntersections import *
from Logic.Measuring.MeasureObject import *

# Directory of RefinedImages
path = "RefinedImages"

# Directory of background image
background_img = "Images/wall.jpg"

# How much pixel blanks will be given after one grid.
grid_interval = 5

image_directory_list = []

for file in os.listdir("Images"):
    image_directory_list.append("Images/" + file)

for item in image_directory_list:

    try:
        # Remove shadows from image
        without_shadow = shadow_remove(cv2.imread(item), cv2.imread(background_img))

        # Apply edge detection to image and find contours
        img_cv2, contour_list = edge_detection(without_shadow)

        # Draw grid on detected image
        grid_img = draw_grid(img_cv2, grid_interval)

        # Find intersection points of gid and image
        horizontal_list, vertical_list = find_intersection(contour_list, grid_interval)

        # Measure object and save final image.
        # Takes Image,ImageName,Image Saving Path, Horizontal Intersection List, Vertical Intersection List
        measure_and_save(grid_img, item[7:], path, horizontal_list, vertical_list)

    except Exception as ex:
        print(ex)
