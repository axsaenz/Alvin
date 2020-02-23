import numpy as np
import cv2
import camera
import images

resolution = .3
img = cv2.imread('Photos/original.jpg')
img_resized = cv2.resize(img, (int(640 * resolution),int(480 * resolution)), interpolation = cv2.INTER_CUBIC)
img_gray = cv2.cvtColor(img_resized, cv2.COLOR_RGB2GRAY)
img_blur = images.gaussian(img_gray, 11)
img_canny = images.canny(img_blur, 100, 130)
imshape = img_resized.shape
vertix0 = (0, imshape[0])
vertix1 = (0, int(333. * imshape[0] / 480.))
vertix2 = (int(200 * imshape[1] / 640), int(65 * imshape[0] / 480))
vertix3 = (int(430 * imshape[1] / 640), int(65 * imshape[0] / 480))
vertix4 = (imshape[1], int(333 * imshape[0] / 480))
vertix5 = (imshape[1], imshape[0])
vertices = np.array([[vertix0, vertix1, vertix2, vertix3, vertix4, vertix5]], dtype = np.int32)
img_region = images.region_of_interest(img_canny, vertices)
try:
	img_hough, lines = images.hough(img_resized, img_region, 2, 15, 2) # To check parameters
except np.linalg.LinAlgError:
	img_hough = img_resized
mask = cv2.inRange(img_hough, np.array([255, 255, 200]), np.array([255, 255, 255]))
final = cv2.bitwise_or(img,
cv2.resize(img_hough, (640, 480), interpolation = cv2.INTER_CUBIC),
	mask = cv2.bitwise_not(cv2.resize(mask, (640, 480), interpolation = cv2.INTER_CUBIC)))
cv2.imshow('final', final)
cv2.waitKey(0)
cv2.imwrite('Photos/original_test_.3.jpg', final)
