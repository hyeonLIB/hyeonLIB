import cv2
import numpy as np
import Hyeon_utils
import math

src = cv2.imread('Lenna.png')

Width, Height = src.shape[0], src.shape[1]
angle_degree = 30  # Set angle degree you want.
angle_radian = angle_degree / 100 * math.pi

new_Width, new_Height =  int(Width * math.cos(angle_radian) + Height * math.sin(angle_radian)), int(Width * math.sin(angle_radian) + Height * math.cos(angle_radian))
dst = np.zeros((new_Width+1, new_Height+1), np.uint8)
print(dst.shape)

for W in range(new_Width):
    for H in range(new_Height):
        xy = Hyeon_utils.cvtCoordinate([H,W], new_Height, new_Width, type='ARRAY_TO_XY')
        rotated = Hyeon_utils.rotation(xy, angle_degree)
        new_xy = Hyeon_utils.cvtCoordinate(rotated, Height, Width, type='XY_TO_ARRAY')
        if (-new_Height < new_xy[0] < new_Height) & (-new_Width < new_xy[1] < new_Width):
            dst[new_xy[0], new_xy[1]] = src[H, W]

cv2.namedWindow('Destination Image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Destination Image', dst)
cv2.namedWindow('Source Image', cv2.WINDOW_AUTOSIZE)
cv2.imshow('Source Image', src)
cv2.waitKey(0)
cv2.destroyAllWindows
cv2.imwrite('result.png', dst)