def find_intersection(contours_list):
    xy_coords = get_xy_list_from_contour(contours_list)
    int_x = find_intersections_x(xy_coords)
    int_y = find_intersections_y(xy_coords)
    return int_x, int_y


def get_xy_list_from_contour(contours):
    full_dataset = []
    for contour in contours:
        xy_list = []
        for position in contour:
            [[x, y]] = position
            xy_list.append([x, y])
        full_dataset.append(xy_list)
    return full_dataset


def find_intersections_x(xy_coords):
    inter_x = list()
    for i in range(len(xy_coords)):
        for j in range(len(xy_coords[i])):
            if xy_coords[i][j][0] % 30 == 0:
                inter_x.append([xy_coords[i][j][0], xy_coords[i][j][1]])
    return inter_x


def find_intersections_y(xy_coords):
    inter_y = list()
    for i in range(len(xy_coords)):
        for j in range(len(xy_coords[i])):
            if xy_coords[i][j][1] % 30 == 0:
                inter_y.append([xy_coords[i][j][0], xy_coords[i][j][1]])
    return inter_y
