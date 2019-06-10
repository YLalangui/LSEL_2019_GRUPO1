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
import time
import struct
import math

from configparser import ConfigParser
from mov_sensor_prueba import*
presencia=0
pos_v=0
pos_h=0
paso=8
data=0
presencia_buf=[1,1,1,1,1,1,1,1]

config = ConfigParser()
config.read("tema.cfg")

def sensor():
	global data
	global pos_v
	global pos_h
	global presencia
	global presencia_buf
	host='172.16.3.42'

	port=5000
	#backlog=5
	size=1024


	#mac1[0:3]=['f','e','1','8'] #mac cupula
	#mac2[0:3]="713c" #mac ultrasonidos

	#mac3[0:3]="ddbc" #mac alfombra

	#server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	#server.bind((host,port))
	#print(1)

	#sock=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	

	print(2)
	#input = [server]
	running=1


	valor_1 = 750
	valor_2 = 750

	#simulamos la coordenada del sensor
	sensor1_v=config.getint("SENSOR_PIR", "sensor1_v")
	sensor1_h=config.getint("SENSOR_PIR", "sensor1_h")
	
	sensor2_v=config.getint("SENSOR_ULTRASONIDO", "sensor2_v")
	sensor2_h=config.getint("SENSOR_ULTRASONIDO", "sensor2_h")

	sensor3_v=config.getint("SENSOR_ALFOMBRA", "sensor3_v")
	sensor3_h=config.getint("SENSOR_ALFOMBRA", "sensor3_h")

	




	t_muestreo=0.15
	kd=0.01
	kp=0.15
	
	paso=1

	while running:
		time.sleep(1)
		"""
		unpacker = struct.Struct('s')
		unpacked_data = unpacker.unpack(data)
		mac_rec[0:3] = unpacked_data[0:3]
		deteccion = unpacked_data[4]
		print(unpacked_data)
		"""
		
		
		# mac1 la leemos del archivo de configuracion y mac_rec es la que recibimos de la wemos
		#if deteccion=="1" and mac1[0:3]==mac_rec[0:3]:
		#print(config.get("SENSOR_POSICION", "mac_1"))
		if data == config.get("SENSOR_PIR", "mac"):
			contador = 0
			#sock.sendto("1", ("172.16.1.1", 8000)) #Envio al NetCat
			print "mover motor"
			movimiento(sensor1_v,sensor1_h)
			valor_v=sensor1_v
			valor_h=sensor1_h
			pos_v_ant=pos_v
			pos_h_ant=pos_h
			time.sleep(1)

			while (1):
				#time.sleep(t_muestreo)
				print("Dentro del bucle")

				d_error_v=(pos_v-pos_v_ant)/t_muestreo
				d_error_h=(pos_v-pos_v_ant)/t_muestreo	
				time.sleep(0.05)

				if  ((pos_v>0)and(pos_h>0) and (valor_v<9000 and valor_h<9000) and (valor_v>0 and valor_h>0)): # v+ h+ mover abajo izqu	
					valor_v=valor_v-paso
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)
					print("Aqui 11111111")
					
				elif ((pos_v>0)and(pos_h<0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v+ h- mover abajo derech
					valor_v=valor_v+paso
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)	
					print("Aqui 22222222")
				elif ((pos_v<0)and(pos_h>0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h+ mover arib izqui
					valor_v=valor_v-paso
					valor_h=valor_h+paso
					movimiento(valor_v,valor_h)
					print("Aqui 3333333")
				elif ((pos_v<0)and(pos_h<0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h- mober arriva derexa 
					valor_v=valor_v+paso
					valor_h=valor_h+paso
					movimiento(valor_v,valor_h)
					print("Aqui 44444444")	


				if  ((pos_v==0)and(pos_h>0) and (valor_v<9000 and valor_h<9000) and (valor_v>0 and valor_h>0)): # v+ h+ mover abajo izqu	
					valor_v=valor_v
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)
					print("Aqui 11111111")
				elif ((pos_v==0)and(pos_h<0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v+ h- mover abajo derech
					valor_v=valor_v
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)	
					print("Aqui 22222222")
				elif ((pos_v<0)and(pos_h==0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h+ mover arib izqui
					valor_v=valor_v-paso
					valor_h=valor_h
					movimiento(valor_v,valor_h)
					print("Aqui 3333333")
				elif ((pos_v>0)and(pos_h==0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h- mober arriva derexa 
					valor_v=valor_v+paso
					valor_h=valor_h
					movimiento(valor_v,valor_h)
					print("Aqui 44444444")		




				if (presencia_buf==[0,0,0,0,0,0,0,0] or data == config.get("SENSOR_ALFOMBRA", "mac")):
					valor_v=750
					valor_h=750
					movimiento(valor_v,valor_h)
					break
				"""
				elif data == config.get("SENSOR_ALFOMBRA", "mac"):

					contador = 0
					sock.sendto("1", ("172.16.1.1", 8000)) #Envio al NetCat
					print "mover motor"
					valor_v=750
					valor_h=750
					movimiento(valor_v,valor_h)
					break
				"""
					

				


		elif data == config.get("SENSOR_ULTRASONIDO", "mac"):

			contador = 0
			#sock.sendto("1", ("172.16.1.1", 8000)) #Envio al NetCat
			print "mover motor"
			movimiento(sensor2_v,sensor2_h)
			valor_v=sensor2_v
			valor_h=sensor2_h
			pos_v_ant=pos_v
			pos_h_ant=pos_h
			time.sleep(1)

			while (1):
				#time.sleep(t_muestreo)
				print("Dentro del bucle")

				d_error_v=(pos_v-pos_v_ant)/t_muestreo
				d_error_h=(pos_v-pos_v_ant)/t_muestreo	
				time.sleep(0.05)	
				if  ((pos_v>0)and(pos_h>0) and (valor_v<9000 and valor_h<9000) and (valor_v>0 and valor_h>0)): # v+ h+ mover abajo izqu	
					valor_v=valor_v-paso
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)
					print("Aqui 11111111")
				elif ((pos_v>0)and(pos_h<0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v+ h- mover abajo derech
					valor_v=valor_v+paso
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)	
					print("Aqui 22222222")
				elif ((pos_v<0)and(pos_h>0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h+ mover arib izqui
					valor_v=valor_v-paso
					valor_h=valor_h+paso
					movimiento(valor_v,valor_h)
					print("Aqui 3333333")
				elif ((pos_v<0)and(pos_h<0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h- mober arriva derexa 
					valor_v=valor_v+paso
					valor_h=valor_h+paso
					movimiento(valor_v,valor_h)
					print("Aqui 44444444")	


				if  ((pos_v==0)and(pos_h>0) and (valor_v<9000 and valor_h<9000) and (valor_v>0 and valor_h>0)): # v+ h+ mover abajo izqu	
					valor_v=valor_v
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)
					print("Aqui 11111111")
				elif ((pos_v==0)and(pos_h<0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v+ h- mover abajo derech
					valor_v=valor_v
					valor_h=valor_h-paso
					movimiento(valor_v,valor_h)	
					print("Aqui 22222222")
				elif ((pos_v<0)and(pos_h==0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h+ mover arib izqui
					valor_v=valor_v-paso
					valor_h=valor_h
					movimiento(valor_v,valor_h)
					print("Aqui 3333333")
				elif ((pos_v>0)and(pos_h==0)and (valor_v<9000 and valor_h<9000)and (valor_v>0 and valor_h>0)): # v- h- mober arriva derexa 
					valor_v=valor_v+paso
					valor_h=valor_h
					movimiento(valor_v,valor_h)
					print("Aqui 44444444")	

				
				if (presencia_buf==[0,0,0,0,0,0,0,0] or data == config.get("SENSOR_ALFOMBRA", "mac")):
					valor_v=750
					valor_h=750
					movimiento(valor_v,valor_h)
					break

				"""
				if (presencia_buf==[0,0,0,0,0,0,0,0]):
					valor_v=750
					valor_h=750
					movimiento(valor_v,valor_h)
					break


				elif data == config.get("SENSOR_ALFOMBRA", "mac"):

					contador = 0
					sock.sendto("1", ("172.16.1.1", 8000)) #Envio al NetCat
					print "mover motor"
					valor_v=750
					valor_h=750
					movimiento(valor_v,valor_h)
					break
				""" 
				




		else:
			print "no hago nada"
			movimiento(valor_1,valor_2)
			#print("Presencia bucle:", presencia)
		


def inicio_camara():

	myCmd='raspivid -t 0 -w 600 -h 400 -hf -ih -fps 20 -o - | nc -k -l 2222'
	os.system(myCmd)

	
def datos_camara():
	global pos_v
	global pos_h
	global presencia

	global presencia_buf
	i=0
	#socket datos camara
	sock_ball=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	sock_ball.bind(('172.16.3.42',8081))
	unpacker = struct.Struct('I f f')
	while 1:
		#time.sleep(2)
		data_ball, addr_ball = sock_ball.recvfrom(1024)
		unpacked_data = unpacker.unpack(data_ball)
		presencia = unpacked_data[0]
		pos_h = unpacked_data[1]
		pos_v = unpacked_data[2]
		presencia_buf[i]=presencia
		i=(i+1) % 8
		
		print (type(presencia))
		print (type(pos_h))
		print (type(pos_v))
		print("presencia: ",presencia," pos_h: ", pos_h," pos_v: ", pos_v)

def lectura():
	
	global data
	host='172.16.3.42'

	port=5000
	#backlog=5
	size=1024


	#mac1[0:3]=['f','e','1','8'] #mac cupula
	#mac2[0:3]="713c" #mac ultrasonidos

	#mac3[0:3]="ddbc" #mac alfombra

	server=socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server.bind((host,port))
	input = [server]
	running=1

	while running:
		print(3)
		data, addr = server.recvfrom(size) #buffer size is 1024 bytes #recepción sensor 
		print(type(data))
	     	print "received message:", data
		data = data.strip()
		time.sleep(0.1)
		


if __name__ == '__main__':

	h1 = threading.Thread(name='sensor', target=sensor)
	h2 = threading.Thread(name='camara', target=inicio_camara)
	h3 = threading.Thread(name='datos_camara', target=datos_camara)
	h4 = threading.Thread(name='lectura', target=lectura)
	h1.start()
	h2.start()
	h3.start()
	h4.start()

