import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

image_src = cv2.imread('book.jpg')

pts_src = np.array([[95,50],[507,28],[55,700],[618,673]], dtype=np.float32)

# Here, I have used L2 norm. You can use L1 also.
width_AD = np.sqrt(((pts_src[0,0] - pts_src[1,0]) ** 2) + ((pts_src[0,1] - pts_src[1,1]) ** 2))
width_BC = np.sqrt(((pts_src[2,0] - pts_src[3,0]) ** 2) + ((pts_src[2,1] - pts_src[3,1]) ** 2))
maxWidth = max(int(width_AD), int(width_BC))


height_AB = np.sqrt(((pts_src[0,0] - pts_src[2,0]) ** 2) + ((pts_src[0,1] - pts_src[2,1]) ** 2))
height_CD = np.sqrt(((pts_src[1,0] - pts_src[3,0]) ** 2) + ((pts_src[1,1] - pts_src[3,1]) ** 2))
maxHeight = max(int(height_AB), int(height_CD))



pts_dst = np.float32([[0, 0],[0, maxHeight - 1],[maxWidth - 1, maxHeight - 1],[maxWidth - 1, 0]])
# pts_src = np.array( [[176,237],[117,221],[254,327]], dtype=np.float32 )

cv2.imshow('book',image_src)
M  = cv2.getPerspectiveTransform(pts_src, pts_dst)

dst = cv2.warpPerspective(image_src,M,(maxWidth, maxHeight),flags=cv2.INTER_LINEAR)

cv2.imshow('dst',dst)
cv2.waitKey(0)
cv2.destroyAllWindows
# T = 2
# fps = 20

# frames = int(T * fps)
# a_list = np.linspace(0,1,frames)

# for a in a_list:
#     pts_temp = pts_src * (1-a) + pts_dst * (a)







# cv2.waitKey(0)
# cv2.destroyAllWindows