import cv2
import numpy as np
import threading
import time
import math

routeChosen = False
mask = None
mask_inv = None
b,g,r = 0,0,0

# mouse callback function
def get_route_mask(event,x,y,flags,param):
	if event == cv2.EVENT_LBUTTONDBLCLK:
		global routeChosen, mask, mask_inv, hsv
		routeChosen = not routeChosen
		if routeChosen:
			color = hsv[y,x]
			lower = np.array([0 if color[0] - 10 < 0 else color[0] - 10, 
							0 if color[1] - 75 < 0 else color[1] - 75,
							0 if color[2] - 75 < 0 else color[2] - 75], np.uint8)
			upper = np.array([180 if color[0] + 10 > 180 else color[0] + 10, 
							255 if color[1] + 75 > 255 else color[1] + 75,
							255 if color[2] + 75 > 255 else color[2] + 75], np.uint8)
			print('point')
			print(color)
			print('upper and lower')
			print(upper)
			print(lower)
			mask = cv2.inRange(hsv, lower, upper)
			mask_inv = cv2.bitwise_not(mask)

def change_color(phase):
	global b,g,r
	b = math.sin((2*math.pi) * (phase/60)) * 127 + 128
	g = math.sin((2*math.pi) * (phase/60) + ((2*math.pi)/3)) * 127 + 128
	r = math.sin((2*math.pi) * (phase/60) + ((4*math.pi)/3)) * 127 + 128

# Create a black image, a window and bind the function to window
img = cv2.imread('wall.jpg', 1)
rows,cols,channels = img.shape
colorImg = np.zeros((rows,cols,3), np.uint8)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
cv2.namedWindow('image')
cv2.setMouseCallback('image', get_route_mask)
phase = 1

while(1):
	if routeChosen:
		imgRoute = cv2.bitwise_and(img, img, mask = mask_inv)
		colorRoute = cv2.bitwise_and(colorImg, colorImg, mask = mask)
		newImg = cv2.add(imgRoute,colorRoute)
		cv2.imshow('image', newImg)
		change_color(phase)
		colorImg[:,:] = (b,g,r)
		if phase == 60:
			phase = 0
		else:
			phase = phase + 1
	else:
		cv2.imshow('image',img)
	if cv2.waitKey(20) & 0xFF == 27:
		break
cv2.destroyAllWindows()