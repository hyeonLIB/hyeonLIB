#%%
import os
os.chdir(os.path.dirname(__file__))
import cv2
import matplotlib.pyplot as plt
import numpy as np

# %% Load two images
image_messi = cv2.imread('messi.jpg')
image_logo = cv2.imread('opencv-logo.jpg')

# margin = 20
def select_color(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse Clicked at {[x,y]} On the Logo")
        selected_pixel = image_logo[y, x, :].copy() 
        print(selected_pixel)

        #**********Homework*************
        #You should program this part to select a color region

        color = 0 # color 값 초기화
        threshold = 50 # threshold 를 기준으로 색을 분류하기 위해 지정
        height, width, _ = image_logo.shape # logo image의 shape에서 높이와 너비 구하기

        """
        어떤 단색을 선택했는지 각 픽셀의 RGB 단색 기준에 따라 (threshold를 기준으로) 확인 후 단색 정의
        color == 0 -> RED
        color == 1 -> GREEN
        color == 2 -> BLUE
        """
        if (selected_pixel[0] < threshold) & (selected_pixel[1] < threshold) & (selected_pixel[2] > threshold): # 선택된 픽셀의 rgb 값들을 threshold를 기준 삼아 분리
            color = 2 # RED
        elif (selected_pixel[0] < threshold) & (selected_pixel[1] > threshold) & (selected_pixel[2] < threshold):
            color = 1 # GREEN
        elif (selected_pixel[0] > threshold) & (selected_pixel[1] < threshold) & (selected_pixel[2] < threshold):
            color = 0 # BLUE
        elif (selected_pixel[0] > threshold) & (selected_pixel[1] > threshold) & (selected_pixel[2] > threshold):
            color = 3 # WHITE

        """
        선택된 컬러에 해당하는 픽셀들의 값들을 0으로 변환하여
        해당 컬러 지우기
        """
        if color == 0: # 선택된 컬러가 Blue 일 경우
            print("Selected color is Blue")
            for i in range(height):
                for j in range(width): 
                    if (image_logo[i,j,0] > threshold) & (image_logo[i,j,1] < threshold) & (image_logo[i,j,2] < threshold): # Blue에 해당하는 컬러의 픽셀 값일 경우
                        image_logo[i,j,:] = 0 # 0으로 변환
        
        elif color == 1: # 선택된 컬러가 Green 일 경우
            print("Selected color is GREEN")
            for i in range(height):
                for j in range(width): 
                    if (image_logo[i,j,0] < threshold) & (image_logo[i,j,1] > threshold) & (image_logo[i,j,2] < threshold): # Green에 해당하는 컬러의 픽셀 값일 경우
                        image_logo[i,j,:] = 0 # 0으로 변환

        elif color == 2: # 선택된 컬러가 Red 일 경우
            print("Selected color is RED")
            for i in range(height):
                for j in range(width): 
                    if (image_logo[i,j,0] < threshold) & (image_logo[i,j,1] < threshold) & (image_logo[i,j,2] > threshold): # Red에 해당하는 컬러의 픽셀 값일 경우
                        image_logo[i,j,:] = 0 # 0으로 변환

        elif color == 3:
            print("Selected color is WHITE")
            for i in range(height):
                for j in range(width):
                    if (image_logo[i,j,0] > threshold) & (image_logo[i,j,1] > threshold) & (image_logo[i,j,2] > threshold):
                        image_logo[i,j,:] = 0

        cv2.imshow('image_logo', image_logo)
        

def add_two_images(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        print(f"Mouse Clicked at {[x,y]} On the Messi")        

        #**********Homework*************
        #You should program this part to select a color region

        m_height, m_width, _ = image_messi.shape # 메시 이미지의 높이와 너비 구하기
        l_height, l_width, _ = image_logo.shape # 로고 이미지의 높이와 너비 구하기
        threshold = 100 # threshold 를 기준으로 이미지의 색 처리

        """
        클릭한 위치 때문에 로고 사이즈를 초과하여 로고가 잘리는 현상을 방지하기 위해
        메시 이미지의 사이즈에서 로고 이미지 사이즈를 뺀 좌표값보다 클릭한 부분의 좌표값이 클 경우
        메시 이미지의 사이즈에서 로고 이미지 사이즈를 뺀 좌표값으로 변환
        """
        if (y > m_height - l_height): # 선택된 y 좌표에 의해 로고 사이즈가 잘리는 경우
            y = m_height - l_height # 잘리지 않는 범위에 있는 좌표로 변환
        if (x > m_width - l_width): # 선택된 x 좌표에 의해 로고 사이즈가 잘리는 경우
            x = m_width - l_width # 잘리지 않는 범위에 있는 좌표로 변환

        """
        마우스 클릭한 좌표부터 이미지를 합성하는 코드
        사이즈가 다른 문제점을 해결하기 위해서 messi_image의 픽셀들을 loop 하는 동안 선택한 좌표가 나온 곳 부터
        선택한 좌표를 뺀 인덱스 값을 logo_image의 좌표값으로 할당.
        좌표값에서 logo_image에서 색이 있는 즉, 픽셀의 RGB 값이 일정 threshold를 넘는 경우
        messi_image의 해당 좌표의 픽셀에 logo_image 픽셀 값을 할당하여 합성.
        """
        for i in range(m_height):
            for j in range(m_width):
                if (y <= i < y+l_height) & (x <= j < x+l_width): # 선택한 좌표에서부터 로고 이미지의 사이즈 범위까지의 좌표인 경우
                    logo_pixel = image_logo[i-y, j-x, :] # loop로 돌아가는 index - 선택된 좌표 == 로고 이미지의 좌표
                    # logo_image에 해당 좌표의 RGB 픽셀 값 중 하나라도 threshold 보다 큰 경우 단색이 있다고 condition 설정
                    condition = (logo_pixel[0] > threshold) | (logo_pixel[1] > threshold) | (logo_pixel[2] > threshold)
                    
                    if condition:
                        image_messi[i,j] = logo_pixel # 해당 좌표에 logo_image의 픽셀 값을 할당
                    else:
                        image_messi[i,j] = image_messi[i,j] + logo_pixel

        cv2.imshow('image_messi', image_messi)

cv2.namedWindow('image_logo', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('image_logo', select_color)

cv2.namedWindow('image_messi', cv2.WINDOW_AUTOSIZE)
cv2.setMouseCallback('image_messi', add_two_images)

cv2.imshow('image_logo', image_logo)
cv2.imshow('image_messi', image_messi)

cv2.waitKey(0)
cv2.destroyAllWindows
# %%
