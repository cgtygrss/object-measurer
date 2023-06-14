from Logic.SaveFile.SaveFile import *
from PIL import Image
import cv2
import random

color_yellow = (0, 255, 255)
color_blue = (255, 0, 0)


def get_distinct_x(xy_coords):
    dist_x = list()
    for i in range(len(xy_coords)):
        if xy_coords[i][0] not in dist_x:
            dist_x.append(xy_coords[i][0])
    return dist_x


def get_distinct_x_coords(xy_coords, dist_x):
    x_coords = list()
    for j in dist_x:
        dist_x_coords = list()
        for i in xy_coords:
            if i not in dist_x_coords and i[0] == j:
                dist_x_coords.append(i)
        x_coords.append(dist_x_coords)
    return x_coords


def get_distinct_y_coords(xy_coords, dist_y):
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


def find_same_dots_on_x(_lists, _l):
    same_dots_x = list()
    for j in range(len(_l)):
        test_list_x = list()
        for i in range(len(_lists)):
            if _lists[i][0] == _l[j]:
                num = _lists[i][1]
                test_list_x.append([num, _l[j]])
        same_dots_x.append([test_list_x])
    return same_dots_x


def find_same_dots_on_y(_lists, _l):
    same_dots_y = list()
    for j in range(len(_l)):
        test_list_y = list()
        for i in range(len(_lists)):
            if _lists[i][1] == _l[j]:
                num = _lists[i][0]
                test_list_y.append([num, _l[j]])
        same_dots_y.append([test_list_y])
    return same_dots_y


def draw_lines_x(_img, x_coords, _color):
    x_coords.sort()
    for k in x_coords:
        k.sort()
        for i in range(len(k) - 1):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            rgb = [r, g, b]
            point1 = k[i]
            if i > 0:
                if k[i][1] - k[i - 1][1] < 10:
                    continue
            for j in range(i + 1, len(k)):
                point2 = k[j]
                if point2[1] - point1[1] >= 25:
                    print(f"{point1} {point2} : {point2[1] - point1[1]}")
                    cv2.line(_img, point1, point2, rgb, 2)
                    cv2.putText(_img, f"{((point2[1] - point1[1]) * 0.1633):.2f}", point2, cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255, 255, 255))
                    break


def draw_lines_y(_img, y_coords, _color):
    y_coords.sort()
    for k in y_coords:
        k.sort()
        for i in range(len(k) - 1):
            r = random.randint(0, 255)
            g = random.randint(0, 255)
            b = random.randint(0, 255)
            rgb = [r, g, b]
            point1 = k[i]
            if i > 0:
                if k[i][0] - k[i - 1][0] < 10:
                    continue
            for j in range(i + 1, len(k)):
                point2 = k[j]
                if point2[0] - point1[0] >= 25:
                    print(f"{point1} {point2} : {point2[0] - point1[0]}")
                    cv2.line(_img, point1, point2, rgb, 2)
                    cv2.putText(_img, f"{((point2[0] - point1[0]) * 0.1633):.2f}", point2, cv2.FONT_HERSHEY_SIMPLEX, 0.1, (255, 255, 255))
                    break


def distance_calculate(p1, p2):
    """p1 and p2 in format (x1,y1) and (x2,y2) tuples"""
    dis = ((p2[0] - p1[0]) ** 2 + (p2[1] - p1[1]) ** 2) ** 0.5
    return dis


def draw_lines(_img, _l, _col):
    for i in range(0, len(_l) - 1, 2):
        point1 = tuple(_l[i])
        point2 = tuple(_l[i + 1])
        cv2.line(_img, point1, point2, _col, 5)


def measure(img, horizontal_list, vertical_list):
    dist_x = get_distinct_x(horizontal_list)
    dist_y = get_distinct_y(vertical_list)

    x_coords = get_distinct_x_coords(horizontal_list, dist_x)
    y_coords = get_distinct_y_coords(vertical_list, dist_y)

    draw_lines_x(img, x_coords, color_blue)
    draw_lines_y(img, y_coords, color_yellow)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    return img_pil
