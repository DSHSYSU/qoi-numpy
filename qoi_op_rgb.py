import numpy as np

def RGB(red, green, blue):
    rgb = np.array([254, red, green, blue], dtype="uint8")
    return rgb

# red = 114
# green = 51
# blue = 4
# RGB = RGB(red, green, blue)