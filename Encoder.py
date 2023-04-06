import cv2
import numpy as np
from create_head import qoi_header
from rgb2rgbline import rgb2rgbline
from qoi_op_diff import Diff
from qoi_op_rgb import RGB
from qoi_op_luma import Luma
import time


def encoder(image):
    [height, width] = qoi_header(image)
    [i_line, i_line_len] = rgb2rgbline(image)
    # i与j用来指向某一个像素，这里进行初始化
    i = 0
    j = 1  # j 指向的像素是待编码的像素
    pixel_prev = i_line[:, i]
    bianma = RGB(red=pixel_prev[0], green=pixel_prev[1], blue=pixel_prev[2])
    while j < i_line_len:
        # 计算前面的像素 i
        pixel_prev = np.array(i_line[:, i])
        # 待编码像素 j
        pixel = np.array(i_line[:, j])
        # 计算一些差值，它们的格式都是uint8
        dr = pixel[0] - pixel_prev[0]
        dg = pixel[1] - pixel_prev[1]
        db = pixel[2] - pixel_prev[2]
        dr_dg = dr - dg
        db_dg = db - dg
        if dr == 0 and dg == 0 and db == 0:
            run = j - i
            j = j + 1
            if run == 62:
                bianma = np.concatenate((bianma, np.array([128 + 64 + run - 1], dtype="uint8")))
                i = j - 1
            elif j == i_line_len - 1 + 1:
                bianma = np.concatenate((bianma, np.array([128 + 64 + run - 1], dtype="uint8")))
                break
        else:  # dr == 0 and dg == 0 and db == 0 不成立的时候
            # 对于行程编码生效的时候，这意味着遇到了第一个像素结束行程编码。
            run = j - i - 1
            if 1 <= run <= 61:  # 前面确有行程编码
                # 行程编码+diff或者luma或者RGB编码
                bianma = np.concatenate((bianma, np.array([128 + 64 + run - 1], dtype="uint8")))
                # 下列三种情况对pixel编码
                if (dr <= 1 or dr >= 254) and (dg <= 1 or dg >= 254) and (db <= 1 or db >= 254):
                    diff = Diff(dr, dg, db)
                    bianma = np.concatenate((bianma, diff))
                    i = j
                    j = j + 1
                elif (dg <= 31 or dg >= 224) and (dr_dg <= 7 or dr_dg >= 248) and (db_dg <= 7 or db_dg >= 248):
                    luma = Luma(dr, dg, db)
                    bianma = np.concatenate((bianma, luma))
                    i = j
                    j = j + 1
                else:
                    rgb = RGB(red=pixel[0], green=pixel[1], blue=pixel[2])
                    bianma = np.concatenate((bianma, rgb))
                    i = j
                    j = j + 1
            if run == 0:
                # 也就是j = i + 1，j紧挨着i，但是pixel和pixel_prev不同，于是执行下列代码
                # 无行程编码，只执行以下diff或者luma或者RGB编码
                if (dr <= 1 or dr >= 254) and (dg <= 1 or dg >= 254) and (db <= 1 or db >= 254):
                    diff = Diff(dr, dg, db)
                    bianma = np.concatenate((bianma, diff))
                    i = j
                    j = j + 1
                elif (dg <= 31 or dg >= 224) and (dr_dg <= 7 or dr_dg >= 248) and (db_dg <= 7 or db_dg >= 248):
                    luma = Luma(dr, dg, db)
                    bianma = np.concatenate((bianma, luma))
                    i = j
                    j = j + 1
                else:
                    rgb = RGB(red=pixel[0], green=pixel[1], blue=pixel[2])
                    bianma = np.concatenate((bianma, rgb))
                    i = j
                    j = j + 1
    return height, width, bianma

start = time.time()
image_dir = "testimg_3.png"
image = cv2.imread(image_dir)
[height, width, bianma] = encoder(image)
end = time.time()
time_len = end - start
