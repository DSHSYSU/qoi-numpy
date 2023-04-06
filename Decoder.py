import cv2
import numpy as np
from Encoder import encoder
import time


def decoder(height, width, bianma):
    np.array(height).astype(int)
    np.array(width).astype(int)
    # 初始化三个通道为空
    image_line_R = np.array([])  # R通道
    image_line_G = np.array([])  # G通道
    image_line_B = np.array([])  # B通道
    # 初始化指向bianma的第0项
    i = 0
    # 把编码变成int
    bianma = np.array(bianma, dtype=int)

    while i < len(bianma):
        bm_i = np.array(bianma[i], dtype=int)
        # bm_i_plus_1 = np.array(bianma[i + 1], dtype=int)
        if bm_i == 254:  # RGB
            image_line_R = np.append(image_line_R, bianma[i + 1])
            image_line_G = np.append(image_line_G, bianma[i + 2])
            image_line_B = np.append(image_line_B, bianma[i + 3])
            i = i + 4
        elif 192 <= bm_i <= 253:  # RUN mode
            run = bm_i - 192 + 1  # run >= 1, <= 62
            run_R = image_line_R[-1] * np.ones(run)
            run_G = image_line_G[-1] * np.ones(run)
            run_B = image_line_B[-1] * np.ones(run)
            image_line_R = np.append(image_line_R, run_R)
            image_line_G = np.append(image_line_G, run_G)
            image_line_B = np.append(image_line_B, run_B)
            i = i + 1
        elif 128 <= bm_i <= 191:  # LUMA mode
            dg = bm_i - 128
            db_dg = bianma[i + 1] % 16
            dr_dg = (bianma[i + 1] - db_dg) / 16
            # 左移32与8，恢复原状
            dg = dg - 32
            db_dg = db_dg - 8
            dr_dg = dr_dg - 8

            dr = dg + dr_dg
            db = dg + db_dg
            image_line_R = np.append(image_line_R, image_line_R[-1] + dr)
            image_line_G = np.append(image_line_G, image_line_G[-1] + dg)
            image_line_B = np.append(image_line_B, image_line_B[-1] + db)
            i = i + 2
        else:  # DIFF mode
            drdgdb = bm_i - 64
            db = drdgdb % 4
            dg = ((drdgdb - db) / 4) % 4
            dr = (drdgdb - 4 * dg - db) / 16
            # 左移2，恢复原状
            dr = dr - 2
            dg = dg - 2
            db = db - 2
            image_line_R = np.append(image_line_R, image_line_R[-1] + dr)
            image_line_G = np.append(image_line_G, image_line_G[-1] + dg)
            image_line_B = np.append(image_line_B, image_line_B[-1] + db)
            i = i + 1
    # 转三通道为uint8
    image_line_R = np.array(image_line_R, dtype="uint8")  # R
    image_line_G = np.array(image_line_G, dtype="uint8")  # G
    image_line_B = np.array(image_line_B, dtype="uint8")  # B
    # 把三行转换为三个矩阵
    image_R = image_line_R.reshape(height, width)
    image_G = image_line_G.reshape(height, width)
    image_B = image_line_B.reshape(height, width)
    # 把三个矩阵合成为RGB图像
    image = np.zeros([height, width, 3], dtype="uint8")
    image[:, :, 0] = image_R
    image[:, :, 1] = image_G
    image[:, :, 2] = image_B
    return image
    # return image_line_R, image_line_G, image_line_B

start = time.time()
image_dir = "testimg_5.png"
image = cv2.imread(image_dir)
[height, width, bianma] = encoder(image)
image_fuyuan = decoder(height, width, bianma)
end = time.time()
time_length = end - start
# [image_line_R, image_line_G, image_line_B] = decoder(height, width, bianma)