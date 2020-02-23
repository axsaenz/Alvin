# Module imports
import numpy as np
import cv2
import images

# Desciption:
#	Class that defines camera properties and processes its images
# Attributes:
#	camera: cv2.VideoCapture object
#	resolution: camera resolution
class Camera:


	def __init__(self, camera_port = 0, resolution = 1):
		self.camera = cv2.VideoCapture('estaaa.webm')
		self.resolution = resolution
		if not self.camera.isOpened():
			raise ValueError('Camera disconnected or wrong port!')
		self.camera.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
		self.camera.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

	# Description:
	#	Destructor, releases the camera
	def __del__(self):
		self.camera.release()
		print('Camera released!')

	# Description:
	#	Returns next frame on camera if there is so
	# Outputs:
	#	img/None: image taken
	def take_photo(self):
		check, img = self.camera.read()
		if check:
			return img
		return None

	# Description:
	#	Reproduces live video from camera
	def live_video(self):
		while True:
			img = self.take_photo()
			cv2.imshow('Live video', img)
			if cv2.waitKey(1) == ord('q'):
				break
		cv2.destroyAllWindows()

	# Description:
	#	Returns processed image of camera's next frame
	# Inputs:
	#	a, b, c: Hough parameters
	# Outputs:
	#	final: processed image
	temp_medio = [0,0,0,0]
	def get_final(self, a = 2, b = 15, c = 2):
		global temp_medio
		img = self.take_photo()
		img_resized = cv2.resize(img, (int(640 * self.resolution),int(480 * self.resolution)), interpolation = cv2.INTER_CUBIC)
		src_coordinates = np.float32(
   			[[0 ,  480],  # Bottom left
     		[220,  150],  # Top left
     		[420,  150],  # Top right
     		[600, 480]]) # Bottom right
		src_coordinates = src_coordinates * self.resolution
		dst_coordinates = np.float32(
    		[[0,  480],  # Bottom left
     		[140,    0],  # Top left
     		[500,   0],  # Top right
     		[640, 480]]) # Bottom right
		dst_coordinates = dst_coordinates * self.resolution
		img_warped, M, Minv = images.warp(img_resized, src_coordinates, dst_coordinates)

		img_gray = cv2.cvtColor(img_warped, cv2.COLOR_RGB2GRAY)
		img_blur = images.gaussian(img_gray, 5)
		img_canny = images.canny(img_blur, 100, 130)
		imshape = img_resized.shape
		height = img_resized.shape[0]
		length = img_resized.shape[1]
		vertix0 =(0,height)
		vertix1 =(0, 80)
		vertix2 = (length, 80)
		vertix3 = (length,height)
		#vertix4 = (imshape[1], int(333 * imshape[0] / 480))
		#vertix5 = (imshape[1], imshape[0])
		vertices = np.array([[vertix0, vertix1, vertix2, vertix3]], dtype = np.int32)

		img_region = images.region_of_interest(img_canny, vertices)

		img_hough, lines = images.hough(img_resized, img_region, a, b, c)
		try:
			medio = np.average(lines, axis = 0) #promedio de
			temp_medio = np.copy(medio)
		except IndexError:
			medio = temp_medio

		carritox1, carritoy1, carritox2, carritoy2 = medio
		mask = cv2.inRange(img_hough, np.array([255, 255, 200]), np.array([255, 255, 255]))
		final0 = cv2.bitwise_or(img,cv2.resize(img_hough, (640, 480), interpolation = cv2.INTER_AREA),mask = cv2.bitwise_not(cv2.resize(mask, (640, 480), interpolation = cv2.INTER_AREA)))

		medio_image = images.punto_medio(img_resized,medio)
		final = cv2.addWeighted(final0, 0.8, medio_image, 1, 1) #mostrar
		return final,carritox1, carritoy1, carritox2, carritoy2,lines
