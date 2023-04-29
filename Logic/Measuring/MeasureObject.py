from Logic.Grid import DrawGrid
from Logic.SpecifyIntersections import SpecifyIntersections
import cv2
from Logic.SaveFile.SaveFile import *

from PIL import Image

color_yellow = (0, 255, 255)
color_blue = (255, 0, 0)


dist_h = list()
dist_v = list()
vertical_points = list()
horizontal_points = list()


def distinct_list_x(lists, _l):
    for i in range(len(lists)):
        if lists[i][0] not in _l:
            _l.append(lists[i][0])


def distinct_list_y(lists, _l):
    for i in range(len(lists)):
        if lists[i][1] not in _l:
            _l.append(lists[i][1])


def find_min_max_dot_x(_lists, _l, _result_list):
    for j in range(len(_l)):
        min = 9999999
        max = -1
        for i in range(len(_lists)):
            if _lists[i][0] == _l[j]:
                num = _lists[i][1]
                if num > max:
                    max = num
                if num < min:
                    min = num
        _result_list.append([_l[j], min])
        _result_list.append([_l[j], max])


def find_min_max_dot_y(_lists, _l, _result_list):
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
        _result_list.append([min, _l[j]])
        _result_list.append([max, _l[j]])


def draw_lines(_img, _l, _col):
    for i in range(0, len(_l) - 1, 2):
        point1 = tuple(_l[i])
        point2 = tuple(_l[i + 1])
        cv2.line(_img, point1, point2, _col, 5)
        print(distance_calculate(point1, point2))


def distance_calculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis


def measure_and_save(img, img_name, path, horizontal_list, vertical_list):

    distinct_list_x(horizontal_list, dist_h)
    distinct_list_y(vertical_list, dist_v)

    find_min_max_dot_x(horizontal_list, dist_h, horizontal_points)
    find_min_max_dot_y(vertical_list, dist_v, vertical_points)

    draw_lines(img, horizontal_points, color_blue)
    draw_lines(img, vertical_points, color_yellow)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    save_image(img_pil, img_name, path)
