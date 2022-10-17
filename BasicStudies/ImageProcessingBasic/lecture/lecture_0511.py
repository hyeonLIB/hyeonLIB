import cv2
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np

source = img.imread("Lenna.png")

def scaling(source, scale, color='color'):
    
    x_axis = int(source.shape[0] * scale)
    y_axis = int(source.shape[1] * scale)
    if color == 'gray':
        image_gray = cv2.cvtColor(source,cv2.COLOR_RGB2GRAY)

        scaled_img = np.zeros((x_axis,y_axis),np.float32)

        for w in range(x_axis):
            for h in range(y_axis):
                w_ = int(w/scale)
                h_ = int(h/scale)
                scaled_img[w,h] = image_gray[w_,h_]

    elif color == 'color':
        scaled_img = np.zeros((x_axis,y_axis,source.shape[2]), np.float32)
        # x_axis = int(source.shape[0] * scale)
        # y_axis = int(source.shape[1] * scale)

        for w in range(x_axis):
            for h in range(y_axis):
                w_ = round(w/scale)
                h_ = round(h/scale)
                scaled_img[w,h] = source[w_,h_]

    else:
        print("color type error")
        return 0

    return scaled_img

scale = 2
scaled_img_color = scaling(source, scale)
# scaled_img_gray = scaling(source, scale, color='gray')
# plt.figure(figsize=(12,10))
plt.imshow(scaled_img_gray, cmap='gray'), plt.title('Scaled iamge')
plt.show()
# plt.imshow(image_gray_color), plt.title('Source image')
# plt.show()