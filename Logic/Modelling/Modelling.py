import numpy
import numpy as np
from stl import mesh
from matplotlib import pyplot
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from PIL import Image
import math

import Data.Object
from Logic.Detecting.Canny import canny
from Logic.Detecting.EdgeDetection import edge_detection
from Logic.Grid.DrawGrid import draw_grid
from Logic.ImageOperations.ImageOperations import convert_image_to_cv2, resize_image, remove_background
from Logic.SpecifyIntersections.SpecifyIntersections import find_intersection

items = ["../../Images/0.jpg", "../../Images/90.jpg"]

objects = []
grey_images = []


for item in items:
    max_size = (500, 500)
    # Remove background of the image
    img = remove_background(item)
    # Convert PIL Image to CV2
    converted_img = convert_image_to_cv2(img)
    # Resize image
    resized_img = resize_image(converted_img, 60)
    # Apply canny edge detection
    canny_img = canny(resized_img)
    # Apply edge detection to image and find contours
    img_cv2, contour_list = edge_detection(canny_img)
    # Find intersection points of grid and image
    horizontal_list, vertical_list = find_intersection(contour_list, 5)
    # Convert image to PIL
    img_pil = Image.fromarray(resized_img)
    grey_img = img_pil.convert("L")
    grey_img.thumbnail(max_size)

    # Get size of an image
    img_height, img_width = grey_img.size

    image_object = Data.Object.ImageObject(img_width, img_height, horizontal_list, vertical_list)

    objects.append(image_object)
    grey_images.append(grey_img)

def create_plate(objects, grey_images):

    max_height = 10
    min_height = 0

    image_np1 = numpy.array(grey_images[0])
    image_np2 = numpy.array(grey_images[1])

    vertices = numpy.zeros((objects[0].width, objects[0].height, 3))
    faces = []

    for x in range(0, objects[0].height):
        for y in range(0, objects[0].width):
            pixel_intensity = image_np2[y][x]
            z = (pixel_intensity * max_height) / image_np2.max()
            vertices[y][x] = (x, y, z)

    for x in range(0, objects[0].height - 1):
        for y in range(0, objects[0].width - 1):
            z = 0
            vertice1 = vertices[y][x]
            vertice2 = vertices[y + 1][x]
            vertice3 = vertices[y + 1][x + 1]
            face1 = np.array([vertice1, vertice2, vertice3])

            vertice4 = vertices[y][x]
            vertice5 = vertices[y][x + 1]
            vertice6 = vertices[y + 1][x + 1]
            face2 = np.array([vertice4, vertice5, vertice6])

            faces.append(face1)
            faces.append(face2)

    facesNp = np.array(faces)

    surface = mesh.Mesh(np.zeros(facesNp.shape[0], dtype=mesh.Mesh.dtype))
    for i, f in enumerate(faces):
        for j in range(3):
            surface.vectors[i][j] = facesNp[i][j]

    surface.save('plate.stl')


create_plate(objects, grey_images)
