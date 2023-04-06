import cv2
import numpy as np

# image_line = np.array(
#     [[184, 208],
#      [204, 235],
#      [215, 252]], dtype="uint8")
dr = 24
dg = 31
db = 37


# luma = 10 11 11 11 00 01 11 10
#             +32       +8
def Luma(dr, dg, db):  # 输入进来的dr dg db都是uint8格式
    dr_dg = dr - dg
    db_dg = db - dg
    # 对dg进行+32的位移
    dg = dg + np.array(32, dtype="uint8")
    # 对dr_dg与db_dg进行+8的位移
    dr_dg = dr_dg + np.array(8, dtype="uint8")
    db_dg = db_dg + np.array(8, dtype="uint8")
    # 生成Byte0与Byte1
    Byte0 = 128 + dg
    Byte1 = 16 * dr_dg + db_dg
    return np.array([Byte0, Byte1], dtype="uint8")


luma = Luma(dr, dg, db)
