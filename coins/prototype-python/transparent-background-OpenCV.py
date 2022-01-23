#!/bin/env python3

import sys, os.path
import cv2 as cv
import numpy as np

seed = (1, 1)
rep_value = (0, 0, 0, 0)
thresh = 15
file = R"../data/record_DE-MUS-062622_kenom_127703/rs.jpg"

# See https://learnopencv.com/filling-holes-in-an-image-using-opencv-python-c/
img = cv.imread(file, cv.IMREAD_COLOR)

th, im_th = cv.threshold(img, 255 - thresh, 255, cv.THRESH_BINARY_INV);
im_floodfill = im_th.copy()
h, w = im_th.shape[:2]
mask = np.zeros((h+2, w+2), np.uint8)

#cv.floodFill(im_floodfill, mask, (seed), 255)
cv.floodFill(im_floodfill, mask, (seed), 255)
im_floodfill_inv = cv.bitwise_not(im_floodfill)
#alpha_mask = (im_th | im_floodfill_inv)[:, :, 0]
alpha_mask = cv.bitwise_or(im_th, im_floodfill_inv)[:, :, 0]

result = img.copy()
result = cv.cvtColor(result, cv.COLOR_RGB2RGBA)
result[:, :, 3] = alpha_mask

cv.imwrite("output.png", result)

cv.imshow("orig", img)
cv.imshow("mask", alpha_mask)
cv.imshow("out", result)

cv.waitKey()
