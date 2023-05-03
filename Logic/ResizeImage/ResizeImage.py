import cv2

scale_percent = 40


def resize_image(param_img):
    # Visualization
    width = int(param_img.shape[1] * scale_percent / 100)
    height = int(param_img.shape[0] * scale_percent / 100)
    dim = (width, height)

    # resize image
    img = cv2.resize(param_img, dim, interpolation=cv2.INTER_AREA)

    return img