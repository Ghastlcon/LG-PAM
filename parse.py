#!/usr/bin/env py
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np

col = [
    (0, 0, 0),
    (255, 255, 255),
    (170, 170, 170),
    (85, 85, 85),
    (254, 211, 199),
    (255, 196, 206),
    (250, 172, 142),
    (255, 139, 131),
    (244, 67, 54),
    (233, 30, 99),
    (226, 102, 158),
    (156, 39, 176),
    (103, 58, 183),
    (63, 81, 181),
    (0, 70, 112),
    (5, 113, 151),
    (33, 150, 243),
    (0, 188, 212),
    (59, 229, 219),
    (151, 253, 220),
    (22, 115, 0),
    (55, 169, 60),
    (137, 230, 66),
    (215, 255, 7),
    (255, 246, 209),
    (248, 203, 140),
    (255, 235, 59),
    (255, 193, 7),
    (255, 152, 0),
    (255, 87, 34),
    (184, 63, 39),
    (121, 85, 72)
]

res = mpimg.imread('res.png')
h = res.shape[0]
w = res.shape[1]
print(h, w)
for i in range(h) :
    for j in range(w) :
        r = int(res[i][j][0] * 256)
        g = int(res[i][j][1] * 256)
        b = int(res[i][j][2] * 256)

        diff = 100000
        pos = -1
        for k in range(32) :
            value = abs(r - col[k][0]) + abs(g - col[k][1]) + abs(b - col[k][2])
            if value < diff:
                diff = value
                pos = k
        print(pos, end = ' ')
    print('')
