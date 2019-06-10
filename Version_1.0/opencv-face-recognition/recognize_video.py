# USAGE
# python recognize_video.py --detector face_detection_model \
#	--embedding-model openface_nn4.small2.v1.t7 \
#	--recognizer output/recognizer.pickle \
#	--le output/le.pickle

# import the necessary packages
from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import argparse
import imutils
import pickle
import time
import cv2
import os
import select
import sys
import socket
import struct

flag = 0
pos_h = 0
pos_v = 0

# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-d", "--detector", required=True,
	help="path to OpenCV's deep learning face detector")
ap.add_argument("-m", "--embedding-model", required=True,
	help="path to OpenCV's deep learning face embedding model")
ap.add_argument("-r", "--recognizer", required=True,
	help="path to model trained to recognize faces")
ap.add_argument("-l", "--le", required=True,
	help="path to label encoder")
ap.add_argument("-c", "--confidence", type=float, default=0.5,
	help="minimum probability to filter weak detections")
args = vars(ap.parse_args())

# load our serialized face detector from disk
print("[INFO] loading face detector...")
protoPath = os.path.sep.join([args["detector"], "deploy.prototxt"])
modelPath = os.path.sep.join([args["detector"],
	"res10_300x300_ssd_iter_140000.caffemodel"])
detector = cv2.dnn.readNetFromCaffe(protoPath, modelPath)

# load our serialized face embedding model from disk
print("[INFO] loading face recognizer...")
embedder = cv2.dnn.readNetFromTorch(args["embedding_model"])

# load the actual face recognition model along with the label encoder
recognizer = pickle.loads(open(args["recognizer"], "rb").read())
le = pickle.loads(open(args["le"], "rb").read())

# initialize the video stream, then allow the camera sensor to warm up
print("[INFO] starting video stream...")
vs = VideoStream(src='tcp://172.16.3.42:2222').start()
#vs = cv2.VideoCapture('tcp://172.16.3.42:2222')
time.sleep(2.0)

# start the FPS throughput estimator
fps = FPS().start()

# loop over frames from the video file stream
while True:
	# grab the frame from the threaded video stream
	frame = vs.read()
	#if frame is not None:
	host='172.16.1.1'
	size=1024
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) # envio aviso jugador
	sock_ball=socket.socket(socket.AF_INET,socket.SOCK_DGRAM) #envio datos reconocimiento y posicion
	sock.sendto("0", ("172.16.0.183", 8080))# para el disparo del jugador (wemos) / Disparo

	# resize the frame to have a width of 600 pixels (while
	# maintaining the aspect ratio), and then grab the image
	# dimensions
	frame = imutils.resize(frame, width=600)
	(h, w) = frame.shape[:2]

	# construct a blob from the image
	imageBlob = cv2.dnn.blobFromImage(
		cv2.resize(frame, (300, 300)), 1.0, (300, 300),
		(104.0, 177.0, 123.0), swapRB=False, crop=False)

	# apply OpenCV's deep learning-based face detector to localize
	# faces in the input image
	detector.setInput(imageBlob)
	detections = detector.forward()
	"""
	# loop over the detections
	for i in range(0, detections.shape[2]):
		# extract the confidence (i.e., probability) associated with
		# the prediction
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		if confidence > args["confidence"]:
			# compute the (x, y)-coordinates of the bounding box for
			# the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")

			# extract the face ROI
			face = frame[startY:endY, startX:endX]
			(fH, fW) = face.shape[:2]

			# ensure the face width and height are sufficiently large
			if fW < 20 or fH < 20:
				continue

			# construct a blob for the face ROI, then pass the blob
			# through our face embedding model to obtain the 128-d
			# quantification of the face
			faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255,
				(96, 96), (0, 0, 0), swapRB=True, crop=False)
			embedder.setInput(faceBlob)
			vec = embedder.forward()

			# perform classification to recognize the face
			preds = recognizer.predict_proba(vec)[0]
			j = np.argmax(preds)
			proba = preds[j]
			name = le.classes_[j]

			# draw the bounding box of the face along with the
			# associated probability
			text = "{}: {:.2f}%".format(name, proba * 100)
			y = startY - 10 if startY - 10 > 10 else startY + 10
			cv2.rectangle(frame, (startX, startY), (endX, endY),
				(0, 0, 255), 2)
			cv2.putText(frame, text, (startX, y),
				cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)
	"""
	# extract the confidence (i.e., probability) associated with
		# the prediction

	
	face_size = np.array([]) # Array donde se van a guardar el area de las caras detectadas
	
	# Este for sirve para iterar sobre las distintas caras que identifica la camara y meter en el array "face_size" el valor de las areas de las caras detectadas
	for i in range(0, detections.shape[2]):
		confidence = detections[0, 0, i, 2]
		if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for
		# the face
			box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
			(startX, startY, endX, endY) = box.astype("int")
			size=abs(endX-startX)*abs(endY-startY)
			face_size = np.append(face_size, size)

	
	# Se mete en la condicion si al menos hay una cara y el tamano de esta sea menor que un umbral (30000)
	if (len(face_size)>0 and abs(endX-startX)*abs(endY-startY)<30000):
		print(abs(endX-startX)*abs(endY-startY))
	
		# Esto es importantisimo: La camara solo va a seguir a una cara y seguira a la mas grande, la que mas area tenga
		# por eso i sera el valor de indice de la cara mas grande entre las que haya detectado la camara, asi no hay problema
		# de averiguar que cara vamos a seguir, se hara un seguimiento de la cara mas grande
		i = np.argmax(face_size)
		confidence = detections[0, 0, i, 2]

		# filter out weak detections
		#if confidence > args["confidence"]:
		# compute the (x, y)-coordinates of the bounding box for
		# the face
		box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
		
		(startX, startY, endX, endY) = box.astype("int")

		# centerX y centerY sera el centro de la cara detectada (Igualmente en la imagen se puede ver el punto que 
		# representa el centro de la cara)
		centerX = (endX+startX)/2
		centerY = (endY+startY)/2
		pos_v = (centerX)-(frame.shape[1]/2)
		pos_v = int(pos_v)
		pos_h = (centerY)-(frame.shape[0]/2)
		pos_h = int(pos_h)
		
		print(pos_v, "pos_v")
		print(pos_h, "pos_h")
		flag = 1
		
		# Esta sentencia dibuja un punto en el medio de la cara
		cv2.circle(frame, (int(centerX), int(centerY)), int(2),(0, 0, 255), 2)
				

		if (centerX > ((frame.shape[1]/2)-20) and centerX < ((frame.shape[1]/2)+20) and centerY> ((frame.shape[0]/2)-20) and centerY < ((frame.shape[0]/2)+20)):
			print("EN EL CENTRO")
			sock.sendto("1", ("172.16.0.183", 8080))# para el disparo del jugador (wemos) / Disparo
########################################## EDITADO
			cv2.line(frame,((frame.shape[1]/2)-20,frame.shape[0]/2),((frame.shape[1]/2)-10,frame.shape[0]/2),(0,255,0),2)
			cv2.line(frame,((frame.shape[1]/2)+10,frame.shape[0]/2),((frame.shape[1]/2)+20,frame.shape[0]/2),(0,255,0),2)

			cv2.line(frame,((frame.shape[1]/2),(frame.shape[0]/2)-20),((frame.shape[1]/2),(frame.shape[0]/2)-10),(0,255,0),2)
			cv2.line(frame,((frame.shape[1]/2),(frame.shape[0]/2)+10),((frame.shape[1]/2),(frame.shape[0]/2)+20),(0,255,0),2)


			cv2.line(frame,((frame.shape[1]/2)-15,(frame.shape[0]/2)+15),((frame.shape[1]/2)-6,(frame.shape[0]/2)+6),(0,255,0),1)
			cv2.line(frame,((frame.shape[1]/2)+6,(frame.shape[0]/2)+6),((frame.shape[1]/2)+15,(frame.shape[0]/2)+15),(0,255,0),1)

			cv2.line(frame,((frame.shape[1]/2)+15,(frame.shape[0]/2)-15),((frame.shape[1]/2)+6,(frame.shape[0]/2)-6),(0,255,0),1)
			cv2.line(frame,((frame.shape[1]/2)-6,(frame.shape[0]/2)-6),((frame.shape[1]/2)-15,(frame.shape[0]/2)-15),(0,255,0),1)
####################################################
		else:

			sock.sendto("0", ("172.16.0.183", 8080))# para el disparo del jugador (wemos) / No disparo

		# extract the face ROI
		face = frame[startY:endY, startX:endX]
		(fH, fW) = face.shape[:2]

		# ensure the face width and height are sufficiently large
		if fW < 20 or fH < 20:
			continue

		# construct a blob for the face ROI, then pass the blob
		# through our face embedding model to obtain the 128-d
		# quantification of the face
		faceBlob = cv2.dnn.blobFromImage(face, 1.0 / 255, (96, 96), (0, 0, 0), swapRB=True, crop=False)
		embedder.setInput(faceBlob)
		vec = embedder.forward()

		# perform classification to recognize the face
		preds = recognizer.predict_proba(vec)[0]
		j = np.argmax(preds)
		proba = preds[j]
		name = le.classes_[j]

		# draw the bounding box of the face along with the
		# associated probability
		text = "{}: {:.2f}%".format(name, proba * 100)
		y = startY - 10 if startY - 10 > 10 else startY + 10
		cv2.rectangle(frame, (startX, startY), (endX, endY),(0, 0, 255), 2)
		cv2.putText(frame, text, (startX, y),cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 255), 2)

	else:
		flag = 0

	# Estas sentencias son las que permite el envio de los valores de flag, pos_v y pos_h
	# Esto esta tal cual en el archivo de ball_tracking, asi que se aconseja no tocarlo mucho
	values = (flag, pos_h,pos_v)
	packer = struct.Struct('I f f')
	packed_data = packer.pack(*values)
	sock_ball.sendto(packed_data,("172.16.3.42", 8081))#revisar socket datos camara



	# update the FPS counter
	fps.update()

	# Esta sentencia dibuja un punto en el centro de la imagen
	#cv2.circle(frame, (int(frame.shape[1]/2), int(frame.shape[0]/2)), int(2),(0, 0, 255), 2)
###################################### EDITADO
	cv2.line(frame,((frame.shape[1]/2)-20,frame.shape[0]/2),((frame.shape[1]/2)-10,frame.shape[0]/2),(0,0,255),2)
	cv2.line(frame,((frame.shape[1]/2)+10,frame.shape[0]/2),((frame.shape[1]/2)+20,frame.shape[0]/2),(0,0,255),2)

	cv2.line(frame,((frame.shape[1]/2),(frame.shape[0]/2)-20),((frame.shape[1]/2),(frame.shape[0]/2)-10),(0,0,255),2)
	cv2.line(frame,((frame.shape[1]/2),(frame.shape[0]/2)+10),((frame.shape[1]/2),(frame.shape[0]/2)+20),(0,0,255),2)
############################

	# show the output frame
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# if the `q` key was pressed, break from the loop
	if key == ord("q"):
		break

# stop the timer and display FPS information
fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))

# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()
