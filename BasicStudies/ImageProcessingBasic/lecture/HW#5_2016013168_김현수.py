import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
import cv2


image_src=cv2.imread('gnu_vi.jpg')

cv2.imshow('src',image_src)

pts_src = np.array([[0,0],[0,291],[464,0],[464,291]], dtype=np.float32)
pts_dst = np.array([[230,3],[0,291],[270,3],[464,291]], dtype=np.float32)


P = cv2.transform(pts_src, pts_dst)
M = cv2.getPerspectiveTransform(pts_src, pts_dst)

dst = cv2.warpPerspective(image_src, M, (image_src.shape[1], image_src.shape[0]))
cv2.imshow('dst', dst)

cv2.waitKey(0)