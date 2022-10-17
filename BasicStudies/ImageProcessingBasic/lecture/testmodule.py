import numpy as np
import math

# def cvt_coordinate(source, scale, color='color'):
    
#     x_axis = int(source.shape[0] * scale)
#     y_axis = int(source.shape[1] * scale)
#     if color == 'gray':
#         image_gray = cv2.cvtColor(source,cv2.COLOR_RGB2GRAY)

#         scaled_img = np.zeros((x_axis,y_axis),np.float32)

#         for w in range(x_axis):
#             for h in range(y_axis):
#                 w_ = int(w/scale)
#                 h_ = int(h/scale)
#                 scaled_img[w,h] = image_gray[w_,h_]

#     elif color == 'color':
#         scaled_img = np.zeros((x_axis,y_axis,source.shape[2]), np.float32)
#         # x_axis = int(source.shape[0] * scale)
#         # y_axis = int(source.shape[1] * scale)

#         for w in range(x_axis):
#             for h in range(y_axis):
#                 w_ = round(w/scale)
#                 h_ = round(h/scale)
#                 scaled_img[w,h] = source[w_,h_]

#     else:
#         print("color type error")
#         return 0

#     return scaled_img





def rotation(x, y, degree):
    theta = degree / 180 * math.pi
    rotation_matrix = np.array([[math.cos(theta), -math.sin(theta)],[math.sin(theta), math.cos(theta)]])
    coordinate = np.array([x,y])
    rotated_coordinate = np.matmul(rotation_matrix, coordinate)
    
    return rotated_coordinate