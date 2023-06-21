import numpy as np


def convert_image_to_cv2(param_image):
    open_cv_image = np.array(param_image)
    # Convert RGB to BGR
    open_cv_image = open_cv_image[:, :, ::-1].copy()

    return open_cv_image
