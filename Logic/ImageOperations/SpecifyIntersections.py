def find_intersections(contours_list, interval):
    coords = get_contour_coordinates(contours_list)
    horizontal_intersections = get_horizontal_intersections(coords, interval)
    vertical_intersections = get_vertical_intersections(coords, interval)
    return horizontal_intersections, vertical_intersections


def get_contour_coordinates(contours):
    coordinates = []
    for contour in contours:
        sub_coordinates = []
        for position in contour:
            [[x, y]] = position
            sub_coordinates.append([x, y])
        coordinates.append(sub_coordinates)
    return coordinates


def get_horizontal_intersections(coords, interval):
    horizontal_intersections = list()
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            if coords[i][j][0] % interval == 0:
                horizontal_intersections.append([coords[i][j][0], coords[i][j][1]])
    return horizontal_intersections


def get_vertical_intersections(coords, interval):
    vertical_intersections = list()
    for i in range(len(coords)):
        for j in range(len(coords[i])):
            if coords[i][j][1] % interval == 0:
                vertical_intersections.append([coords[i][j][0], coords[i][j][1]])
    return vertical_intersections
