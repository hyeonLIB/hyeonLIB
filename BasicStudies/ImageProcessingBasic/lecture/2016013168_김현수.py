import os
os.chdir(os.path.dirname(__file__))
import cv2
import matplotlib.pyplot as plt
import numpy as np

H = 400
R = 100

w_square = 255*np.ones([H,H,3])

def Click(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Left Mouse Clicked at {[x,y]}")
        for i in range(H):
            for j in range(H):
                if clac_dist_to_center(i - y + R/2, j - x + R/2, R/2, R/2) <= R: 
                    paint_blue(i,j, w_square)

    if event == cv2.EVENT_RBUTTONDOWN:
        print(f"Right Mouse Clicked at {[x,y]}")
        for i in range(H):
            for j in range(H):
                if (y - R <= i < y + R) & (x - R <= j < x + R):
                    paint_red(i,j, w_square)

    cv2.imshow('Midterm_exam', w_square)

def clac_dist_to_center(x, y, a, b):
    return np.sqrt((x-a)**2 + (y-b)**2)

def paint_black(x, y, image):
    image[x, y, 0] = 0
    image[x, y, 1] = 0
    image[x, y, 2] = 0
    return image

def paint_red(x, y, image):
    image[x, y, 0] = 0
    image[x, y, 1] = 0
    image[x, y, 2] = 255

def paint_blue(x,y,image):
    image[x,y,0] = 255
    image[x,y,1] = 0
    image[x,y,2] = 0


for x in range(H):
    for y in range(H):
        if clac_dist_to_center(x, y, H/2, H/2) <= R:
            w_square = paint_black(x,y, w_square)


cv2.namedWindow('Midterm_exam', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('Midterm_exam', Click)
cv2.imshow('Midterm_exam', w_square)

cv2.waitKey(0)
cv2.destroyAllWindows