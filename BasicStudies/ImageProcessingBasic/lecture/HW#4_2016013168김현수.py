import cv2
import numpy as np
import Hyeon_utils

src = cv2.imread('Lenna.png')

Width, Height = src.shape[0], src.shape[1]
dst = np.zeros_like(src)
angle_degree = 30  # Set angle degree you want.

for W in range(Width):
    for H in range(Height):
        xy = Hyeon_utils.cvtCoordinate([H,W], Height, Width, type='ARRAY_TO_XY')
        rotated = Hyeon_utils.rotation(xy, angle_degree)
        new_xy = Hyeon_utils.cvtCoordinate(rotated, Height, Width, type='XY_TO_ARRAY')
        if (-Height < new_xy[0] < Height) & (-Width < new_xy[1] < Width):
            dst[new_xy[0], new_xy[1]] = src[H, W]

cv2.namedWindow('Destination Image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Destination Image', dst)
cv2.namedWindow('Source Image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Source Image', src)
cv2.waitKey(0)
cv2.destroyAllWindows
cv2.imwrite('result.png', dst)