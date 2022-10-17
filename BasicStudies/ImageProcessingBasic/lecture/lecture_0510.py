import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

image = img.imread("image_complex.png")
plt.figure(figsize=(12,10))
plt.imshow(image), plt.title('Original Image')

image_hsv = cv2.cvtColor(image, cv2.COLOR_RGB2HSV)

image_gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
plt.figure(figsize=(12,10))
plt.imshow(image_gray, cmap='gray'), plt.title('Gray Image')

# Threshold
ret, image_thresh = cv2.threshold(image_gray,50,255,cv2.THRESH_BINARY_INV)
plt.figure(figsize=(12,10))
plt.imshow(image_thresh,cmap='gray'), plt.title('Threshold')

mask_size = 5
mask = np.ones((mask_size, mask_size), np.float32)/(mask_size**2)
image_open = cv2.morphologyEx(image_thresh, cv2.MORPH_OPEN, mask, iterations=0)

plt.figure(figsize=(12,10))
plt.imshow(image_open, cmap='gray'), plt.title('Open')

image_close = cv2.morphologyEx(image_open, cv2.MORPH_CLOSE, mask, iterations=0)
plt.figure(figsize=(12,10))
plt.imshow(image_close, cmap='gray'), plt.title('Close')

contours, _ = cv2.findContours(
    image_close,
    mode=cv2.RETR_LIST,
    method=cv2.CHAIN_APPROX_SIMPLE
)
image_copy = image.copy()

cv2.drawContours(image_copy, contours=contours, \
    contoursIdx=-1, color=(0,255,0),thickness=2)
plt.figure(figsize=(12,10))
plt.imshow(image_copy, cmap='gray'), plt.title('Contours Detected')

perimiters = []
areas = []
for c in contours:
    perimeter = cv2.arcLength(c,closed=True) # 둘레 길이 측정
    perimeters.append(perimeter)
    area =cv2.contourArea(c)
    areas.append(area)

# Find contours by area greater than a threshold
th_area = 0
image_copy = image.copy()
cnt = 0
contours_final = []
for i in range(len(areas)):
    if areas[i] > th_area:
        cnt += 1
        contours_final.append(contours[i])

cv2.drawContours(image_copy, contours_final, \
    contourIdx=-1, color=(0,255,0), thickness=2)

plt.figure(figsize=(12,10))
plt.imshow(image_copy, cmap='gray'), plt.title('Contours Selected by Area')
print(f'Total:{cnt}')




# import cv2
# import matplotlib.pyplot as plt
# import matplotlib.image as img
# import numpy as np

# source = img.imread("Lenna.png")
# image_gray = cv2.cvtColor(source,cv2.COLOR_RGB2GRAY)

# scale = 2
# x_axis = int(source.shape[0] * scale)
# y_axis = int(source.shape[1] * scale)

# scaled_img = np.zeros((x_axis,y_axis),np.float32)

# for w in range(x_axis):
#     for h in range(y_axis):
#         w_new = int(w/scale)
#         h_new = int(h/scale)
#         scaled_img[w,h] = image_gray[w_new,h_new]

# plt.imshow(scaled_img, cmap='gray'), plt.title('Scaled iamge')
# plt.show()