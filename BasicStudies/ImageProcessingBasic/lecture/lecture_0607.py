import dlib
import numpy as np
import cv2
import matplotlib.pyplot as plt


detector = dlib.get_frontal_face_detector()
img = cv2.imread('woman.jpg')
img = cv2.resize(img, dsize=(300, 300), interpolation=cv2.INTER_CUBIC)
det = detector(img)

print(det)

width, height = img.shape[0], img.shape[1]

# [[(x1, y1), (x2, y2)]] = det
for detected in det:
    [(x1, y1), (x2, y2)] = detected
    img = cv2.rectangle(img, detected, (0, 255, 0), 3)






# for h in range(height):
#     for w in range(width):
#         if ((54 <= w <= 234) & (273 <= h <= 274)) or ((54 <= w <= 234) & (94 <= h <= 95)):
#             img[w,h] = [0,255,0]
#         elif  or (w >= 54 & w <= 234 & h == 273) or (w == 54 & h >= 94 & h <= 273) or (w == 234 & h >= 94 & h <= 273):
cv2.imshow('img',img)
cv2.waitKey(0)










# def detecting(image):
#     img = cv2.resize(image, dsize=(300,300), interpolation=cv2.INTER_CUBIC)
#     det = detector(img)
#     width, height = img.shape[0], img.shape[1]
#     print(det)
#     if det == True:

#     # [[(x1, y1), (x2, y2)]] = det
#     # img = cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 3)
#     # for w in range(width):
#     #     for h in range(height):
#     #         if (w>=54):
#     #             img[w,h] = [0,255,0]
    
#     return img



# cam = cv2.VideoCapture(0)
# while True:
#     ret,frame = cam.read()
#     if ret:
#         detected_frame = detecting(frame)
#         cv2.imshow('Detected frame', detected_frame)
#         if cv2.waitKey(1) & 0xFF == ord('q'):
#             break
#     else:
#         pass