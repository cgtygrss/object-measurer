from Logic.Utils.ListUtil import get_sub_lists
from Logic.ImageOperations.SpecifyIntersections import get_distinct_x_intersections


def calculate_object_height_pixel_ratio(contour_list, interval, object_height):
    coords = get_sub_lists(contour_list)
    distinct_x_intersections = get_distinct_x_intersections(coords, interval)
    min_y = min(distinct_x_intersections)
    max_y = max(distinct_x_intersections)

    pixel_ratio = object_height / (max_y - min_y)

    return pixel_ratio
