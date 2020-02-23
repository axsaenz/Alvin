import numpy as np
from numpy.linalg import norm
import cv2
import camera
import images
#import serial


camera_port = int(input('Camera port: '))
resolution = float(input('Resolution: '))
a, b, c = 100, 20, 50
print('Values:', '\na:', a, '\nb:', b, '\nc:', c)
objCamera = camera.Camera(camera_port = camera_port, resolution = resolution)
#with serial.Serial('/dev/ttyUSB0', 9600, timeout=10) as ser:
accion = 'f'
while True:

		final,carritox1, carritoy1, carritox2, carritoy2,lines = objCamera.get_final(a = a, b = b, c = c)
		cv2.imshow('Live video ', final)

		ref = [320,400]

		m = (carritoy2 - carritoy1)/(carritox2 - carritox1)
		print(m)
		try:
			if (lines[0,0]==100) and (lines[1,0]==100):
				accion='d'
			elif (lines[0,0]==600) and (lines[1,0]==600):
				accion='i'
			else:
				if ((m > 1) and ( m < 100)) or ((m < -8) and ( m > -100)) :
					accion = 'a'
				elif (m > -8) and ( m < 0) :
					accion = 'd'
				elif (m <=1) and ( m >= 0) :
					accion = 'i'
				else:
					accion = accion
		except TypeError:
			pass

		print("lines:",lines)

#		if accion in 'a':
#			ser.write(bytes('a\n'))
#		if accion in 'r':
#			ser.write(bytes('r\n'))
#		if accion in 'd':
#			ser.write(bytes('d\n'))
#		if accion in 'i':
#			ser.write(bytes('i\n'))

		print(accion)



		keyPressed = cv2.waitKey(1)
		if keyPressed == ord('q'):
			break
		elif keyPressed == ord('r'):
			print('Actual resolution:', objCamera.resolution)
			objCamera.resolution = float(input('New resolution: '))
		elif keyPressed == ord('a'):
			print('Actual value of a:', a)
			a = int(input('New a: '))
		elif keyPressed == ord('b'):
			print('Actual value of b:', b)
			b = int(input('New b: '))
		elif keyPressed == ord('c'):
			print('Actual value of c:', c)
			c = int(input('New c: '))
