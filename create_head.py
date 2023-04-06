import torch
import cv2
import numpy as np

def qoi_header(image):
    [height, width, channels] = image.shape
    height = np.array(height, dtype=int)
    width = np.array(width, dtype=int)
    return height, width



# image_dir = "testimg.png"
# image = cv2.imread(image_dir)
# [height, width] = qoi_header(image)