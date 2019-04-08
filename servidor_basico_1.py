#!/usr/bin/python
# -*- coding: iso-8859-15 -*-



"""
A simple echo server
"""

import socket
import sys
import select
import pickle
import threading
import os


from mov_sensor_prueba import*


def sensor():

	host='172.16.3.42'

	port=5000
	#backlog=5
	size=1024

	server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server.bind((host,port))
	print(1)
	sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)

	print(2)
	input = [server]
	running=1
	

	valor_1 = 750
	valor_2 = 750

	#simulamos la coordenada del sensor
	sensor1_v=1200
	sensor1_h=900

	sensor2_v=1200
	sensor2_h=480


	while running:
		print(3)
		data, addr = server.recvfrom(size) #buffer size is 1024 bytes
	     	print "received message:", data

		data = data.strip()

		if data=="1":

			sock.sendto("1", ("172.16.1.1", 8000))
			print "mover motor"
			movimiento(sensor1_v,sensor1_h)
		
		else:
			print "no hago nada"
			movimiento(valor_1,valor_2)


def camara():
	myCmd='raspivid -t 0 -w 600 -h 400 -hf -ih -fps 20 -o - | nc -k -l 2222'
	os.system(myCmd)


if __name__ == '__main__':

	h1 = threading.Thread(name='sensor', target=sensor)
	h2 = threading.Thread(name='camara', target=camara)
	h1.start()
	h2.start()

