import numpy as np
import cv2
import camera
import images


objCamera = camera.Camera(camera_port = 1, resolution = 1)
img = objCamera.take_photo()
gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
cv2.imshow('Gray', gray)
cv2.waitKey(0)

gray_blur = images.gaussian(gray, 11)
cv2.imshow('Gaussian', gray_blur)
cv2.waitKey(0)

gray_canny = images.canny(gray_blur, 100, 130)
cv2.imshow('Canny', gray_canny)
cv2.waitKey(0)

imshape = img.shape
vertix0 = (0, imshape[0])
vertix1 = (0, int(333 * imshape[0] / 480))
vertix2 = (int(200 * imshape[1] / 640), int(65 * imshape[0] / 480))
vertix3 = (int(430 * imshape[1] / 640), int(65 * imshape[0] / 480))
vertix4 = (imshape[1], int(333 * imshape[0] / 480))
vertix5 = (imshape[1], imshape[0])
vertices = np.array([[vertix0, vertix1, vertix2, vertix3, vertix4, vertix5]], dtype=np.int32)
region = images.region_of_interest(gray_canny, vertices)
cv2.imshow('Region', region)
cv2.waitKey(0)

hough = images.hough(img, region, 0, 0, 120)
cv2.imshow('Hough', hough)
cv2.waitKey(0)

camera.save_photo('hough', hough)

cv2.destroyAllWindows()