import numpy as np


# image_line = np.array(
#     [[184, 185],
#      [204, 202],
#      [215, 216]],dtype="uint8")

# diff = 01 11 00 10
def Diff(dr, dg, db):  # 输入进来的dr dg db都是uint8格式
    dr = dr + np.array(2, dtype="uint8")
    dg = dg + np.array(2, dtype="uint8")
    db = db + np.array(2, dtype="uint8")
    diff = 64 + 16 * dr + 4 * dg + db
    diff = np.array([diff], dtype="uint8")
    return diff
# dr = 1
# dg = -2
# db = 0
# diff = Diff(dr, dg, db)
