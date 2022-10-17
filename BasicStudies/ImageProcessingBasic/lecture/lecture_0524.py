import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

image_src = cv2.imread('hillary.jpg')
image_dst = cv2.imread('woman.jpg')

pts_src = np.array( [[176,237],[117,221],[254,327]], dtype=np.float32 )
pts_dst = np.array( [[193,240],[322,239],[245,330]], dtype=np.float32 )

cv2.imshow('hillary',image_src)
cv2.imshow('woman',image_dst)

T = 2
fps = 20

frames = int(T * fps)
a_list = np.linspace(0,1,frames)

for a in a_list:
    pts_temp = pts_src * (1-a) + pts_dst * (a)







cv2.waitKey(0)
cv2.destroyAllWindows