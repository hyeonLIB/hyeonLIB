import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

src = cv2.imread('image_cell.png')
src_bnw = src[:,:,0]
binary = np.ones_like(src_bnw) * 255

for h in range(src_bnw.shape[0]):
    for w in range(src_bnw.shape[1]):
        if src_bnw[h,w] < 50:
            binary[h,w] = src_bnw[h,w]

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

src_dst1 = erode_dil(src_bnw, 3, 'erode')
src_dst2 = erode_dil(src_bnw, 3, 'dilation')

for h in range(src_dst1.shape[0]):
    for w in range(src_dst1.shape[1]):
        if src_dst1[h,w] < 50:
            binary[h,w] = src_dst1[h,w]

def cnt_obj():
    stack = [row, col]
    while stack:
        idx = stack.pop()

        if checked[idx[0], idx[1]] == 1:
            continue

        checked[idx[0], idx[1]] = 1
        obj_id_matrix[idx[0], idx[1]] = obj_cnt
        [idxs_y, idxs_x] = np.meshgrid[np.arange(idx[1]-1, idx[1]+1)]
        for i in range(idxs_x.shape[0]):
            for j in range(idxs_y.shape[1]):
                if idxs_x[i,j] < 0 or idxs_y[i,j] > rows-1 or idxs_y[i,j] > rows+1:
                    continue
                elif checked[idxs_x[i,j], idxs_y[i,j]] == 1:
                    continue
                elif img_input[idxs_x[i,j], idxs_y[i,j]] == background:
                    continue
                else:
                    stack.append([idxs_x[i,j], idxs_y[i,j]])

        obj_cnt += 1
    return obj_id_matrix

plt.imshow(binary, cmap='gray')
plt.show()