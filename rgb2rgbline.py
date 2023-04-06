import cv2
import numpy as np

def rgb2rgbline(image):
    image_0 = image[:, :, 0]
    image_1 = image[:, :, 1]
    image_2 = image[:, :, 2]
    i_line_0 = np.array([image_0]).reshape(1, -1)
    i_line_1 = np.array([image_1]).reshape(1, -1)
    i_line_2 = np.array([image_2]).reshape(1, -1)
    i_line = np.concatenate(
        (i_line_0, i_line_1, i_line_2),
        axis=0
    )
    i_line_length = i_line_0.size
    return i_line, i_line_length

image_dir = "testimg.png"
image = cv2.imread(image_dir)
[image_line, image_line_length] = rgb2rgbline(image)