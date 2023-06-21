def get_sub_lists(_list):
    unpacked_list = []
    for sub_list in _list:
        sub_coordinates = []
        for position in sub_list:
            [[x, y]] = position
            sub_coordinates.append([x, y])
        unpacked_list.append(sub_coordinates)
    return unpacked_list
