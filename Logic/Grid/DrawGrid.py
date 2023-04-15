import os
import cv2
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as plticker


# choose where to store images
path = "../../RefinedImages"


try:
    from PIL import Image
except ImportError:
    import Image


def DrawGrid(param_img):

    my_dpi = 150.

    # Get the size of an Image
    width, height = param_img.size

    # Set up figure
    fig = plt.figure(figsize=(float(width)/my_dpi, float(height)/my_dpi), dpi=my_dpi)
    ax = fig.add_subplot(111)

    # Remove whitespace from around the image
    fig.subplots_adjust(left=0, right=1, bottom=0, top=1)

    # Set the griding interval: here we use the major tick interval
    myInterval = 50.
    loc = plticker.MultipleLocator(base=myInterval)
    ax.xaxis.set_major_locator(loc)
    ax.yaxis.set_major_locator(loc)

    # Add the grid
    ax.grid(which='major', axis='both', linestyle='-', color='r')

    # Add the image
    ax.imshow(param_img)

    # Find number of grid squares in x and y direction
    nx = abs(int(float(ax.get_xlim()[1]-ax.get_xlim()[0])/float(myInterval)))
    ny = abs(int(float(ax.get_ylim()[1]-ax.get_ylim()[0])/float(myInterval)))

    print(nx)
    print(ny)

    fig.savefig(f"{path}/grid.jpg")
