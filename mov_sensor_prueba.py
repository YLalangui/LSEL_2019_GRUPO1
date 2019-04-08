import time
#from time import sleep

# Librerias a importar para hacer uso de la camara
from collections import deque
import numpy as np
import argparse


valor_1 = 750
valor_2 = 750

#simulamos la coordenada del sensor
sensor1_v=1200
sensor1_h=900

sensor2_v=1200
sensor2_h=480
	
flag_sensor1=1
flag_sensor2=0

active_f = open("/sys/class/lse-pwm/pwm/active", "rw+")
active_f.write('1')
active_f.close()

frequency_f = open("/sys/class/lse-pwm/pwm/frequency", "rw+")
frequency_f.write('50')
frequency_f.close()

duty_f = open("/sys/class/lse-pwm/pwm/duty", "rw+")
duty_f.write(str(valor_1))
duty_f.close()

active_f_2 = open("/sys/class/lse-pwm_2/pwm/active", "rw+")
active_f_2.write('1')
active_f_2.close()

frequency_f_2 = open("/sys/class/lse-pwm_2/pwm/frequency", "rw+")
frequency_f_2.write('50')
frequency_f_2.close()


duty_f_2 = open("/sys/class/lse-pwm_2/pwm/duty", "rw+")
duty_f_2.write(str(valor_2))
duty_f_2.close()


valor_1 = 750
valor_2 = 750

#simulamos la coordenada del sensor
sensor1_v=1200
sensor1_h=900

sensor2_v=1200
sensor2_h=480

flag_sensor1=1
flag_sensor2=0

active_f = open("/sys/class/lse-pwm/pwm/active", "rw+")
active_f.write('1')
active_f.close()

frequency_f = open("/sys/class/lse-pwm/pwm/frequency", "rw+")
frequency_f.write('50')
frequency_f.close()

duty_f = open("/sys/class/lse-pwm/pwm/duty", "rw+")
duty_f.write(str(valor_1))
duty_f.close()

active_f_2 = open("/sys/class/lse-pwm_2/pwm/active", "rw+")
active_f_2.write('1')
active_f_2.close()

frequency_f_2 = open("/sys/class/lse-pwm_2/pwm/frequency", "rw+")
frequency_f_2.write('50')
frequency_f_2.close()


duty_f_2 = open("/sys/class/lse-pwm_2/pwm/duty", "rw+")
duty_f_2.write(str(valor_2))
duty_f_2.close()



def movimiento(sensor_v,sensor_h):

		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1=sensor_v
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()

		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2=sensor_h
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()
"""
	elif flag_sensor2:
		
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1=sensor2_v
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()

		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2=sensor2_h
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()
	else 
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1=750
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()

		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2=750
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()
"""


"""
print("1")

while True:
	
	time.sleep(2)
      
	if flag_sensor1 :

		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1=sensor1_v
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()

		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2=sensor1_h
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()

	elif flag_sensor2:
		
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1=sensor2_v
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()

		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2=sensor2_h
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()		
      			
	time.sleep(2)
	flag_sensor1=not flag_sensor1
	flag_sensor2=not flag_sensor2

	"""     		









