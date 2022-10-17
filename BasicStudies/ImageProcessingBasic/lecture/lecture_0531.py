import matplotlib.image as img
import matplotlib.pyplot as plt
import numpy as np
import cv2


src = cv2.imread('fft_test.jpeg')
fft = abs(src)
ffted = np.fft.fft2(fft)
ffted = np.array(ffted, dtype='uint8')

shifted = np.fft.fftshift(fft)
shifted = np.array(shifted, dtype='uint8')


cv2.imshow('dst', ffted)

cv2.waitKey(0)