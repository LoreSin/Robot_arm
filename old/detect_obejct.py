import cv2
import numpy as np

cam = cv2.VideoCapture(1)






while True:
	ret, frame = cam.read()
#	cv2.imshow('frame', frame)

	key = cv2.waitKey(10)
	lower_blue = (100, 100, 100)
	upper_blue = (140, 255, 255)
	lower_green = (30, 80, 80)
	upper_green = (70, 255, 255)
	lower_orange = (0, 180, 55)
	upper_orange = (20, 255,200)

	img_hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
	img_mask = cv2.inRange(img_hsv, lower_blue, upper_blue)
	img_result = cv2.bitwise_and(frame, frame, mask = img_mask)
	cv2.imshow('orange', img_result)

	if key == 27:
		break


cv2.destroyAllWindows()
