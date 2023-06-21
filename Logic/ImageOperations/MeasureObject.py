from PIL import Image
import cv2
from Logic.Utils.ColorUtil import generate_random_color


def draw_horizontal_lines(_img, y_coords, pixel_ratio):
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


def draw_vertical_lines(_img, x_coords, pixel_ratio):
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


def measure(img, horizontal_intersection_coords, vertical_intersection_coords, pixel_ratio):
    draw_horizontal_lines(img, horizontal_intersection_coords, pixel_ratio)
    draw_vertical_lines(img, vertical_intersection_coords, pixel_ratio)

    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    img_pil = Image.fromarray(img)

    return img_pil
