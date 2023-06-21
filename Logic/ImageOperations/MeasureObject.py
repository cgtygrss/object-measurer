from PIL import Image
import cv2
from Logic.Utils.ColorUtil import generate_random_color


def get_horizontal_intersection_coords(coords, distinct_y_intersections):
    horizontal_intersection_coords = list()
    for j in distinct_y_intersections:
        distinct_y_coords = list()
        for i in coords:
            if i not in distinct_y_coords and i[0] == j:
                distinct_y_coords.append(i)
        horizontal_intersection_coords.append(distinct_y_coords)
    return horizontal_intersection_coords


def get_vertical_intersection_coords(coords, distinct_x_intersections):
    vertical_intersection_coords = list()
    for j in distinct_x_intersections:
        distinct_x_coords = list()
        for i in coords:
            if i not in distinct_x_coords and i[1] == j:
                distinct_x_coords.append(i)
        vertical_intersection_coords.append(distinct_x_coords)
    return vertical_intersection_coords


def get_distinct_y_intersections(coords):
    distinct_y_intersections = list()
    for i in range(len(coords)):
        if coords[i][0] not in distinct_y_intersections:
            distinct_y_intersections.append(coords[i][0])
    return distinct_y_intersections


def get_distinct_x_intersections(coords):
    distinct_x_intersections = list()
    for i in range(len(coords)):
        if coords[i][1] not in distinct_x_intersections:
            distinct_x_intersections.append(coords[i][1])
    return distinct_x_intersections


def draw_y_lines(_img, y_coords, pixel_ratio):
    y_coords.sort()
    for k in y_coords:
        k.sort()
        for i in range(len(k) - 1):
            point1 = k[i]
            point2 = k[i + 1]
            if point2[1] - point1[1] >= 25:
                print(f"{point1} {point2} : {point2[1] - point1[1]}")
                cv2.line(_img, point1, point2, generate_random_color(), 2)
                distance = calculate_horizontal_distance(point1, point2, pixel_ratio)
                cv2.putText(_img, distance, point1, cv2.FONT_HERSHEY_COMPLEX, 0.5, (255, 0, 0))


def draw_x_lines(_img, x_coords, pixel_ratio):
    x_coords.sort()
    for k in x_coords:
        k.sort()
        for i in range(len(k) - 1):
            point1 = k[i]
            point2 = k[i + 1]
            if point2[0] - point1[0] >= 25:
                print(f"{point1} {point2} : {point2[0] - point1[0]}")
                cv2.line(_img, point1, point2, generate_random_color(), 2)
                distance = calculate_vertical_distance(point1, point2, pixel_ratio)
                cv2.putText(_img, distance, (point2[0] + 20, point2[1]), cv2.FONT_HERSHEY_COMPLEX, 0.5, (0, 0, 0))


def calculate_vertical_distance(p1, p2, pixel_ratio):
    dis = f"{((p2[0] - p1[0]) * pixel_ratio):.2f}"
    return dis


def calculate_horizontal_distance(p1, p2, pixel_ratio):
    dis = f"{((p2[1] - p1[1]) * pixel_ratio):.2f}"
    return dis


def calculate_object_height_pixel_ratio(vertical_list, object_height):
    distinct_x_intersections = get_distinct_x_intersections(vertical_list)
    min_y = min(distinct_x_intersections)
    max_y = max(distinct_x_intersections)

    pixel_ratio = object_height / (max_y - min_y)

    return pixel_ratio


def measure(img, horizontal_list, vertical_list, pixel_ratio):
    distinct_y_intersections = get_distinct_y_intersections(horizontal_list)
    distinct_x_intersections = get_distinct_x_intersections(vertical_list)

    horizontal_intersection_coords = get_horizontal_intersection_coords(horizontal_list, distinct_y_intersections)
    vertical_intersection_coords = get_vertical_intersection_coords(vertical_list, distinct_x_intersections)

    draw_y_lines(img, horizontal_intersection_coords, pixel_ratio)
    draw_x_lines(img, vertical_intersection_coords, pixel_ratio)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    return img_pil
