from Logic.Grid import DrawGrid
from Logic.SpecifyIntersections import SpecifyIntersections
import cv2
from Logic.SaveFile.SaveFile import *

from PIL import Image

color_yellow = (0, 255, 255)
color_blue = (255, 0, 0)


def get_distinct_x(xy_coords):
    dist_x = list()
    for i in range(len(xy_coords)):
        if xy_coords[i][0] not in dist_x:
            dist_x.append(xy_coords[i][0])
    return dist_x


def get_distinct_y(xy_coords):
    dist_y = list()
    for i in range(len(xy_coords)):
        if xy_coords[i][1] not in dist_y:
            dist_y.append(xy_coords[i][1])
    return dist_y


def find_min_max_dot_x(_lists, _l):
    min_max_x = list()
    for j in range(len(_l)):
        min = 9999999
        max = -1
        for i in range(len(_lists)):
            if _lists[i][0] == _l[j]:
                num = _lists[i][1]
                if _lists[i][1] > max:
                    max = num
                if num < min:
                    min = num
        min_max_x.append([_l[j], min])
        min_max_x.append([_l[j], max])
    return min_max_x


def find_min_max_dot_y(_lists, _l):
    min_max_y = list()
    for j in range(len(_l)):
        min = 9999999
        max = -1
        for i in range(len(_lists)):
            if _lists[i][1] == _l[j]:
                num = _lists[i][0]
                if num > max:
                    max = num
                if num < min:
                    min = num
        min_max_y.append([min, _l[j]])
        min_max_y.append([max, _l[j]])
    return min_max_y


def draw_lines(_img, _l, _col):
    for i in range(0, len(_l) - 1, 2):
        point1 = tuple(_l[i])
        point2 = tuple(_l[i + 1])
        cv2.line(_img, point1, point2, _col, 5)
        # print(distance_calculate(point1, point2))


def distance_calculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis


def measure_and_save(img, img_name, path, horizontal_list, vertical_list):
    dist_x = get_distinct_x(horizontal_list)
    dist_y = get_distinct_y(vertical_list)

    min_max_x = find_min_max_dot_x(horizontal_list, dist_x)
    min_max_y = find_min_max_dot_y(vertical_list, dist_y)

    draw_lines(img, min_max_x, color_blue)
    draw_lines(img, min_max_y, color_yellow)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    save_image(img_pil, img_name, path)
