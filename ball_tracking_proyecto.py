# Jose Antonio Fernandez / Yerhard Lalangui
# USAGE
# python ball_tracking.py --video ball_tracking_example.mp4
# python ball_tracking.py

# import the necessary packages
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

flag = 0

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())

# define the lower and upper boundaries of the "green"
# ball in the HSV color space, then initialize the
# list of tracked points
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# if a video path was not supplied, grab the reference
# to the webcam
if not args.get("video", False):
	camera = cv2.VideoCapture('tcp://172.16.3.42:2222')

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])





#!/usr/bin/python
# -*- coding: utf-8 -*-
 
# Ejemplo cliente - servidor en python
# Programa Cliente
# www.elfreneticoinformatico.com

#import socket #utilidades de red y conexion

#declaramos las variables
#ipServidor = "172.16.1.1" #es lo mismo que "localhost" o "0.0.0.0"
#puertoServidor = 9798

#Configuramos los datos para conectarnos con el servidor
#socket.AF_INET para indicar que utilizaremos Ipv4
#socket.SOCK_STREAM para utilizar TCP/IP (no udp)
#Estos protocolos deben ser los mismos que en el servidor
#cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#cliente.connect((ipServidor, puertoServidor))
#print("Conectado con el servidor ---> %s:%s" %(ipServidor, puertoServidor))










# keep looping
while True:




	
    	





	# grab the current frame
	(grabbed, frame) = camera.read()

	# if we are viewing a video and we did not grab a frame,
	# then we have reached the end of the video
	if args.get("video") and not grabbed:
		break

	# resize the frame, blur it, and convert it to the HSV
	# color space
	frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# construct a mask for the color "green", then perform
	# a series of dilations and erosions to remove any small
	# blobs left in the mask
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	# find contours in the mask and initialize the current
	# (x, y) center of the ball
	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
		cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	#Generacion de lineas para los cuadrantes
        cv2.line(frame, (200,0), (200, frame.shape[0]), (255,0,0), 2)
	cv2.line(frame, (400,0), (400, frame.shape[0]), (255,0,0), 2)
	cv2.line(frame, (0, frame.shape[0]/3), (frame.shape[1], frame.shape[0]/3), (255,0,0), 2)
	cv2.line(frame, (0, 2*frame.shape[0]/3), (frame.shape[1], 2*frame.shape[0]/3), (255,0,0), 2)



	# only proceed if at least one contour was found
	if len(cnts) > 0:
		# find the largest contour in the mask, then use
		# it to compute the minimum enclosing circle and
		# centroid
		c = max(cnts, key=cv2.contourArea)
		((x, y), radius) = cv2.minEnclosingCircle(c)
		M = cv2.moments(c)
		center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

		# only proceed if the radius meets a minimum size
		if radius > 10:
			if (x > 200 and x < 400 and y> (frame.shape[0]/3) and y < (2*frame.shape[0]/3)):
				cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
				cv2.circle(frame, center, 5, (0, 255, 0), -1)
				flag = 1
				#break
			else :
				cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
				cv2.circle(frame, center, 5, (0, 0, 255), -1)
				flag = 0

	# update the points queue
	pts.appendleft(center)
	print(flag)
	


	#cliente.send(str(flag))
    	#respuesta = cliente.recv(4096)
    	#print(respuesta)
    	#if respuesta == "exit":
        #	break;



	# loop over the set of tracked points
	for i in xrange(1, len(pts)):
		# if either of the tracked points are None, ignore
		# them
		if pts[i - 1] is None or pts[i] is None:
			continue

		# otherwise, compute the thickness of the line and
		# draw the connecting lines
		if (x > 200 and x < 400 and y > (frame.shape[0]/3) and y < (2*frame.shape[0]/3)):
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 255, 0), thickness)
		else:
			thickness = int(np.sqrt(args["buffer"] / float(i + 1)) * 2.5)
			cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)


	# show the frame to our screen
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the 'q' key is pressed, stop the loop
	if key == ord("q"):
		break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
print("------- CONEXION CERRADA ---------")
#socketServidor.close()
