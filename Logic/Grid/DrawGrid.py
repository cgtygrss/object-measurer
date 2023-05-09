import cv2


def draw_grid(img, grid_interval, line_color=(0, 0, 255), thickness=1, type_=cv2.LINE_AA):
    x = grid_interval
    y = grid_interval
    while x < img.shape[1]:
        cv2.line(img, (x, 0), (x, img.shape[0]), color=line_color, lineType=type_, thickness=thickness)
        x += grid_interval

    while y < img.shape[0]:
        cv2.line(img, (0, y), (img.shape[1], y), color=line_color, lineType=type_, thickness=thickness)
        y += grid_interval

    return img
