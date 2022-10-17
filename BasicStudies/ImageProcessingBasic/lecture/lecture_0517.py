# import cv2
# import matplotlib.pyplot as plt
# import matplotlib.image as img
import numpy as np
import testmodule

# src = cv2.imread('Lenna.png')

# dst = cv2.resize(src, dsize=(640,480), interpolation=cv2.INTER_AREA)
# dst2 = cv2.resize(src, dsize=(0,0), fx=0.3, fy=0.7, interpolation=cv2.INTER_LINEAR)

# cv2.imshow('src',src)
# cv2.imshow('dst', dst)
# cv2.imshow('dst2',dst2)
# cv2.namedWindow('Test', cv2.WINDOW_NORMAL)
# cv2.waitKey(0)
# cv2.destroyAllWindows()

# src = cv2.imread('Lenna.png')
x = 10
y = 2
rotated = testmodule.rotation(x,y,70)

print(rotated)

# cv2.imshow('src',src)
# cv2.imshow('rotated',rotated)
# cv2.namedWindow('Test', cv2.WINDOW_NORMAL)
# cv2.waitKey(0)
# cv2.destroyAllWindows()