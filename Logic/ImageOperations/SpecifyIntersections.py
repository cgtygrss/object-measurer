from Logic.Utils.ListUtil import get_sub_lists


def find_intersections(contours_list, interval):
    coords = get_sub_lists(contours_list)
    distinct_x_intersections = get_distinct_x_intersections(coords, interval)
    distinct_y_intersections = get_distinct_y_intersections(coords, interval)
    horizontal_intersections = get_horizontal_intersection_coords(coords, distinct_y_intersections)
    vertical_intersections = get_vertical_intersection_coords(coords, distinct_x_intersections)
    return horizontal_intersections, vertical_intersections


def get_distinct_y_intersections(coords, interval):
    distinct_y_intersections = list()
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            if coords[i][j][0] not in distinct_y_intersections and coords[i][j][0] % interval == 0:
                distinct_y_intersections.append(coords[i][j][0])
    return distinct_y_intersections


def get_distinct_x_intersections(coords, interval):
    distinct_x_intersections = list()
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            if coords[i][j][1] not in distinct_x_intersections and coords[i][j][1] % interval == 0:
                distinct_x_intersections.append(coords[i][j][1])
    return distinct_x_intersections


def get_horizontal_intersection_coords(coords, distinct_y_intersections):
    horizontal_intersection_coords = list()
    for j in distinct_y_intersections:
        distinct_y_coords = list()
        for i in coords:
            for k in i:
                if i not in distinct_y_coords and k[0] == j:
                    distinct_y_coords.append(k)
            horizontal_intersection_coords.append(distinct_y_coords)
    return horizontal_intersection_coords


def get_vertical_intersection_coords(coords, distinct_x_intersections):
    vertical_intersection_coords = list()
    for j in distinct_x_intersections:
        distinct_x_coords = list()
        for i in coords:
            for k in i:
                if i not in distinct_x_coords and k[1] == j:
                    distinct_x_coords.append(k)
            vertical_intersection_coords.append(distinct_x_coords)
    return vertical_intersection_coords
