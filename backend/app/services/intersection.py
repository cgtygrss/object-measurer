from typing import List, Tuple


def unpack_contours(contour_list: list) -> List[List[List[int]]]:
    """Unpack OpenCV contour format into simple coordinate lists."""
    unpacked = []
    for sub_list in contour_list:
        coords = []
        for point in sub_list:
            [[x, y]] = point
            coords.append([x, y])
        unpacked.append(coords)
    return unpacked


def get_distinct_y_intersections(coords: List[List[List[int]]], interval: int) -> List[int]:
    """Find distinct Y-axis intersection points at given interval."""
    distinct = []
    for contour in coords:
        for point in contour:
            if point[0] not in distinct and point[0] % interval == 0:
                distinct.append(point[0])
    return sorted(distinct)


def get_distinct_x_intersections(coords: List[List[List[int]]], interval: int) -> List[int]:
    """Find distinct X-axis intersection points at given interval."""
    distinct = []
    for contour in coords:
        for point in contour:
            if point[1] not in distinct and point[1] % interval == 0:
                distinct.append(point[1])
    return sorted(distinct)


def get_horizontal_intersection_coords(
    coords: List[List[List[int]]], distinct_y: List[int]
) -> List[List[List[int]]]:
    """Get horizontal intersection coordinates for each Y value."""
    result = []
    for y_val in distinct_y:
        y_coords = []
        for contour in coords:
            for point in contour:
                if point not in y_coords and point[0] == y_val:
                    y_coords.append(point)
        if y_coords:
            result.append(y_coords)
    return result


def get_vertical_intersection_coords(
    coords: List[List[List[int]]], distinct_x: List[int]
) -> List[List[List[int]]]:
    """Get vertical intersection coordinates for each X value."""
    result = []
    for x_val in distinct_x:
        x_coords = []
        for contour in coords:
            for point in contour:
                if point not in x_coords and point[1] == x_val:
                    x_coords.append(point)
        if x_coords:
            result.append(x_coords)
    return result


def find_intersections(
    contour_list: list, interval: int
) -> Tuple[List[List[List[int]]], List[List[List[int]]]]:
    """
    Find intersection points between contour edges and measurement grid.

    Returns:
        Tuple of (horizontal_intersections, vertical_intersections)
    """
    coords = unpack_contours(contour_list)
    distinct_x = get_distinct_x_intersections(coords, interval)
    distinct_y = get_distinct_y_intersections(coords, interval)
    horizontal = get_horizontal_intersection_coords(coords, distinct_y)
    vertical = get_vertical_intersection_coords(coords, distinct_x)
    return horizontal, vertical
