from Logic.SaveFile.SaveFile import *
from PIL import Image
import cv2
import random

color_yellow = (0, 255, 255)
color_blue = (255, 0, 0)

r = random.randint(0, 200)
g = random.randint(0, 200)
b = random.randint(0, 200)
rgb = [r, g, b]


def get_distinct_x(xy_coords):
    dist_x = list()
    for i in range(len(xy_coords)):
        if xy_coords[i][0] not in dist_x:
            dist_x.append(xy_coords[i][0])
    return dist_x


def get_x_coords(xy_coords, dist_x):
    x_coords = list()
    for j in dist_x:
        dist_x_coords = list()
        for i in xy_coords:
            if i not in dist_x_coords and i[0] == j:
                dist_x_coords.append(i)
        x_coords.append(dist_x_coords)
    return x_coords


def get_y_coords(xy_coords, dist_y):
    y_coords = list()
    for j in dist_y:
        dist_y_coords = list()
        for i in xy_coords:
            if i not in dist_y_coords and i[1] == j:
                dist_y_coords.append(i)
        y_coords.append(dist_y_coords)
    return y_coords


def get_distinct_y(xy_coords):
    dist_y = list()
    for i in range(len(xy_coords)):
        if xy_coords[i][1] not in dist_y:
            dist_y.append(xy_coords[i][1])
    return dist_y


def draw_lines_x(_img, x_coords, pixel_ratio):
    x_coords.sort()
    for k in x_coords:
        k.sort()
        for i in range(len(k) - 1):
            point1 = k[i]
            point2 = k[i + 1]
            if point2[1] - point1[1] < 10:
                continue
            if point2[1] - point1[1] >= 25:
                print(f"{point1} {point2} : {point2[1] - point1[1]}")
                cv2.line(_img, point1, point2, rgb, 2)
                distance = distance_calculate_horizontal(point1, point2, pixel_ratio)
                cv2.putText(_img, distance, point1, cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))
                continue


def draw_lines_y(_img, y_coords, pixel_ratio):
    y_coords.sort()
    for k in y_coords:
        k.sort()
        for i in range(len(k) - 1):
            point1 = k[i]
            point2 = k[i + 1]
            if point2[0] - point1[0] < 10:
                continue
            if point2[0] - point1[0] >= 25:
                print(f"{point1} {point2} : {point2[0] - point1[0]}")
                cv2.line(_img, point1, point2, rgb, 2)
                distance = distance_calculate_vertical(point1, point2, pixel_ratio)
                cv2.putText(_img, distance, (point2[0] + 20, point2[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


def distance_calculate_vertical(p1, p2, pixel_ratio):
    dis = f"{((p2[0] - p1[0]) * pixel_ratio):.2f}"
    return dis


def distance_calculate_horizontal(p1, p2, pixel_ratio):
    dis = f"{((p2[1] - p1[1]) * pixel_ratio):.2f}"
    return dis


def calculate_object_height_pixel_ratio(vertical_list, object_height):
    distinct_y_values = get_distinct_y(vertical_list)
    min_y = min(distinct_y_values)
    max_y = max(distinct_y_values)

    pixel_ratio = object_height / (max_y - min_y)

    return pixel_ratio


def measure(img, horizontal_list, vertical_list, pixel_ratio):
    dist_x = get_distinct_x(horizontal_list)
    dist_y = get_distinct_y(vertical_list)

    x_coords = get_x_coords(horizontal_list, dist_x)
    y_coords = get_y_coords(vertical_list, dist_y)

    draw_lines_x(img, x_coords, pixel_ratio)
    # draw_lines_y(img, y_coords, pixel_ratio)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    return img_pil
