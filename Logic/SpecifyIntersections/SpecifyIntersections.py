vertical_list = list()
horizontal_list = list()


def find_intersection(contours_list, grid_interval):
    for i in range(len(contours_list[0])):
        # cv2.circle(img, (contours_list[i][0][0][0], contours_list[i][0][0][1]), 2, (255, 0, 0), -1)
        if contours_list[0][i][0][1] % grid_interval == 0:
            vertical_list.append([contours_list[0][i][0][0], contours_list[0][i][0][1]])
            # cv2.circle(img, (contours_list[0][i][0][0], contours_list[0][i][0][1]), 2, (255, 0, 0), -1)
        if contours_list[0][i][0][0] % grid_interval == 0:
            horizontal_list.append([contours_list[0][i][0][0], contours_list[0][i][0][1]])
            # cv2.circle(img, (contours_list[0][i][0][0], contours_list[0][i][0][1]), 2, (0, 0, 0), -1)

    return horizontal_list, vertical_list
