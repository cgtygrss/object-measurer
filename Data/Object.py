class Object:
    def __init__(self, name, width, length, height):
        self.name = name
        self.width = width
        self.length = length
        self.height = height


class ImageObject:
    def __init__(self, width, height, horizontal_list, vertical_list):
        self.width = width
        self.height = height
        self.HorizontalList = horizontal_list
        self.VerticalList = vertical_list
