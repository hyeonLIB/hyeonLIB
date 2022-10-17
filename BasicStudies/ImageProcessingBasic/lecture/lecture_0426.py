import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import cv2

# 완벽하게 이해하세요 제발 !
src = cv2.imread("image_bolt.png")
src_bnw = src[:,:,0]

def erode_dil(src, mask_size, type):
    src_dst = np.zeros_like(src)
    mask_size = mask_size
    space = int((mask_size-1)/2)

    for h in range(space, src.shape[0]-space):
        for w in range(space, src.shape[1]-space):
            roi = src[h-space:h+space+1, w-space:w+space+1]
            if type == 'dilation':
                src_dst[h,w] = np.max(np.max(roi,axis=0),axis=0)
            elif type == 'erode':
                src_dst[h,w] = np.min(np.min(roi,axis=0),axis=0)
            else:
                print("error")
        
    return src_dst


for i in range(3):
    if i == 0:
        src_dst1 = erode_dil(src_bnw, 3, 'erode')
    else:
        src_dst1 = erode_dil(src_dst1, 3, 'erode')

for i in range(3):
    if i == 0:
        src_dst1 = erode_dil(src_bnw, 3, 'dilation')
    else:
        src_dst1 = erode_dil(src_dst1, 3, 'dilation')
        
plt.imshow(src_dst1, cmap='gray')
plt.show()
# plt.imshow(src_dst2, cmap='gray')
# plt.show()