from time import sleep
from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
sense = SenseHat()

# Librerias a importar para hacer uso de la camara

from collections import deque
import numpy as np
import argparse
import imutils
import cv2

# Librerias a importar para usar sonido
import RPi.GPIO as GPIO
import time

###############################################################
############# INICIALIZACION DE ARRAYS DE SONIDOS #############
###############################################################

buzzer_pin = 27

notes = {
	'B0' : 31,
	'C1' : 33, 'CS1' : 35,
	'D1' : 37, 'DS1' : 39,
	'EB1' : 39,
	'E1' : 41,
	'F1' : 44, 'FS1' : 46,
	'G1' : 49, 'GS1' : 52,
	'A1' : 55, 'AS1' : 58,
	'BB1' : 58,
	'B1' : 62,
	'C2' : 65, 'CS2' : 69,
	'D2' : 73, 'DS2' : 78,
	'EB2' : 78,
	'E2' : 82,
	'F2' : 87, 'FS2' : 93,
	'G2' : 98, 'GS2' : 104,
	'A2' : 110, 'AS2' : 117,
	'BB2' : 123,
	'B2' : 123,
	'C3' : 131, 'CS3' : 139,
	'D3' : 147, 'DS3' : 156,
	'EB3' : 156,
	'E3' : 165,
	'F3' : 175, 'FS3' : 185,
	'G3' : 196, 'GS3' : 208,
	'A3' : 220, 'AS3' : 233,
	'BB3' : 233,
	'B3' : 247,
	'C4' : 262, 'CS4' : 277,
	'D4' : 294, 'DS4' : 311,
	'EB4' : 311,
	'E4' : 330,
	'F4' : 349, 'FS4' : 370,
	'G4' : 392, 'GS4' : 415,
	'A4' : 440, 'AS4' : 466,
	'BB4' : 466,
	'B4' : 494,
	'C5' : 523, 'CS5' : 554,
	'D5' : 587, 'DS5' : 622,
	'EB5' : 622,
	'E5' : 659,
	'F5' : 698, 'FS5' : 740,
	'G5' : 784, 'GS5' : 831,
	'A5' : 880, 'AS5' : 932,
	'BB5' : 932,
	'B5' : 988,
	'C6' : 1047, 'CS6' : 1109,
	'D6' : 1175, 'DS6' : 1245,
	'EB6' : 1245,
	'E6' : 1319,
	'F6' : 1397, 'FS6' : 1480,
	'G6' : 1568, 'GS6' : 1661,
	'A6' : 1760, 'AS6' : 1865,
	'BB6' : 1865,
	'B6' : 1976,
	'C7' : 2093, 'CS7' : 2217,
	'D7' : 2349, 'DS7' : 2489,
	'EB7' : 2489,
	'E7' : 2637,
	'F7' : 2794, 'FS7' : 2960,
	'G7' : 3136, 'GS7' : 3322,
	'A7' : 3520, 'AS7' : 3729,
	'BB7' : 3729,
	'B7' : 3951,
	'C8' : 4186, 'CS8' : 4435,
	'D8' : 4699, 'DS8' : 4978
}

disparo_melody = [
  2500,2400,2300,2200,2100,2000,1900,1800,1700,1600,1500,1400,1300,1200,1100,1000
]

disparo_tempo = [
  75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75
 
]


impacto_melody = [
  97,109,79,121,80,127,123,75,119,96,71,101,98,113,92,70,114,75,86,103,126,118,128,77,114,119,72

]

impacto_tempo = [
  75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75,75

]

################################################################
########## FIN INICIALIZACION DE ARRAYS DE SONIDO ##############
################################################################



###############################################################
############ DECLARACION DE FUNCIONES DE SONIDO ###############
###############################################################

def buzz(frequency, length):	 #create the function "buzz" and feed it the pitch and duration)

	if(frequency==0):
		time.sleep(length)
		return
	period = 1.0 / frequency 		 #in physics, the period (sec/cyc) is the inverse of the frequency (cyc/sec)
	delayValue = period / 2		 #calcuate the time for half of the wave
	numCycles = int(length * frequency)	 #the number of waves to produce is the duration times the frequency
	
	for i in range(numCycles):		#start a loop from 0 to the variable "cycles" calculated above
		GPIO.output(buzzer_pin, True)	 #set pin 27 to high
		time.sleep(delayValue)		#wait with pin 27 high
		GPIO.output(buzzer_pin, False)		#set pin 27 to low
		time.sleep(delayValue)		#wait with pin 27 low
	


def setup():
	GPIO.setmode(GPIO.BCM)
	GPIO.setup(buzzer_pin, GPIO.IN)
	GPIO.setup(buzzer_pin, GPIO.OUT)
	
def destroy():
	GPIO.cleanup()				# Release resource
	

def play(melody,tempo,pause,pace=0.800):
	
	for i in range(0, len(melody)):		# Play song
		
		noteDuration = pace/tempo[i]
		buzz(melody[i],noteDuration)	# Change the frequency along the song note
		
		pauseBetweenNotes = noteDuration * pause
		time.sleep(pauseBetweenNotes)
	
def sonido_disparo():
	try:
		setup()
		play(disparo_melody, disparo_tempo, 1.3, 0.800)
		time.sleep(2)
		destroy()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

def sonido_impacto():
	try:
		setup()
		play(impacto_melody, impacto_tempo, 1.3, 0.800)
		time.sleep(2)
		destroy()
	except KeyboardInterrupt:  	# When 'Ctrl+C' is pressed, the child program destroy() will be  executed.
		destroy()

###################################################################
############ FIN DECLARACION DE FUNCIONES DE SONIDO ###############
###################################################################




################################################################
############# CODIGO PARA ARGUMENTOS DE LA CAMARA ##############
#################################################################

# Esta parte solo sirve para leer argumentos en caso de que los haya
# pero en nuestro caso no va a haber argumentos
ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
	help="path to the (optional) video file")
ap.add_argument("-b", "--buffer", type=int, default=64,
	help="max buffer size")
args = vars(ap.parse_args())


# Este cacho es solo para decirle al algoritmo los tonos de 
# verde que quiero que identifique. Ademas inicializa los puntos a trackear
greenLower = (29, 86, 6)
greenUpper = (64, 255, 255)
pts = deque(maxlen=args["buffer"])

# Si no se pasa ningun argumento entonces se captura directamente lo que
# provenga de la camara. Es como una inicializacion a que la camara
# empiece a funcionar
if not args.get("video", False):
	camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
	camera = cv2.VideoCapture(args["video"])

# Lo escrito hasta ahora es pura paja, dentro del while es donde
# esta la chicha para que la camara empiece a funcionar


#############################################################
############ FIN DEL CODIGO PARA ARGUMENTOS DE LA CAMARA######
##############################################################


#globa = 0
paso = 28 # Se Corresponde con 10 grados

sense.clear()
valor_1 = 750
valor_2 = 750

def abajo():
	global valor_1
	
	if valor_1<999:
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1+=paso
		print(valor_1)
		print("abajo")
		duty.write(str(valor_1))
		duty.close()

	

def arriba():
	global valor_1
	if valor_1>500:
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+")
		valor_1-=paso
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()
def izquierda():
	global valor_2
	if valor_2<999:
		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2+=paso
		print(valor_2)
		print("izquierda")
		duty.write(str(valor_2))
		duty.close()

def derecha():
	global valor_2
	if valor_2>500:
		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2-=paso
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()


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


print("1")

while True:

	###################################################################################
	####### INICIO CODIGO PARA CAPTURAR FRAME Y DIBUJAR LAS LINEAS DE LIMITACION ######
	###################################################################################

	# Pilla el frame actual(Teneis que cuidar el sleep que hay al final)
	# Si el sleep es muy grande se tomara un frame por cada tiempo de sleep
	# Si el sleep es mas pequeno pues habra mas frames por segundo
	(grabbed, frame) = camera.read()

	# Si se esta viendo el video pero no se coge ningun frame significara
	# que el video ha terminado
	if args.get("video") and not grabbed:
		break

	# Para los mas curiosos: Pilla el frame y le hace pasar por un filtro
	# que emborrona la imagen para faciliar su procesado. Luego lo hace
	# pasar al espacio de color hsv (en vez de rgb)  No todo es RGB eh?
	# Pero en este caso no se hace pasar por ese filro, ya que ese paso esta comentado
	frame = imutils.resize(frame, width=600)
	# blurred = cv2.GaussianBlur(frame, (11, 11), 0)
	hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

	# Creacion de mascara, inicializacion del contorno y definicion del centro
	mask = cv2.inRange(hsv, greenLower, greenUpper)
	mask = cv2.erode(mask, None, iterations=2)
	mask = cv2.dilate(mask, None, iterations=2)

	cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)[-2]
	center = None

	# Creacion de las dichosas lineas azules que delimitan los cuadrantes
	cv2.line(frame, (200,0), (200, frame.shape[0]), (255,0,0), 2)
	cv2.line(frame, (400,0), (400, frame.shape[0]), (255,0,0), 2)
	cv2.line(frame, (0, frame.shape[0]/3), (frame.shape[1], frame.shape[0]/3), (255,0,0), 2)
	cv2.line(frame, (0, 2*frame.shape[0]/3), (frame.shape[1], 2*frame.shape[0]/3), (255,0,0), 2)



	###################################################################################
	####### FIN DE CODIGO PARA CAPTURAR FRAME Y DIBUJAR LAS LINEAS DE LIMITACION ######
	###################################################################################


	for event in sense.stick.get_events():
		if event.action == ACTION_PRESSED:
      
			if event.direction == "up":
				sense.show_letter("U")      # UP arrow
				arriba()
				
      			elif event.direction == "down":
        			sense.show_letter("D")      # Down arrow
				abajo()

      			elif event.direction == "left": 
        			sense.show_letter("L")      # Left arrow
				izquierda()
				
	      		elif event.direction == "right":
				sense.show_letter("R")      # Right arrow
				derecha()

	      		elif event.direction == "middle":

				sonido_disparo()

      			##########################################################################
      			############# CODIGO DE LA CAMARA CUANDO SE REALIZA EL DISPARO ###########
      			##########################################################################

      			# Aqui comienza el juego chavales, cuando se pulsa el boton del
      			# medio es cuando empiza a ejecutarse el algoritmo que detecta la bolita
        		
        		# El algoritmo se ejecuta si detecta un contorno (la bola) en la camara
        		# independientemente si esta en el centro o no
        			if len(cnts) > 0:

        			# Calculo del contorno de la bola y de su centro
					c = max(cnts, key=cv2.contourArea)
					((x, y), radius) = cv2.minEnclosingCircle(c)
					M = cv2.moments(c)
					center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))

					# (El radio es solo para poner un limite minimo a partir del cual se va a detectar la bola
					# es decir, que si la bola esta muy lejos, aunque este en la camara no se va a detectar)
					if radius > 10:

						# ESTO ES LA CLAVE:
						# Si esta en el centro (delimitado anteriormente por las lineas de delimination):
						# Imprime un 1 y lo rodea con un circulo verde
						if (x > 200 and x < 400 and y> (frame.shape[0]/3) and y < (2*frame.shape[0]/3)):
							cv2.circle(frame, (int(x), int(y)), int(radius),(0, 255, 0), 2)
							cv2.circle(frame, center, 5, (0, 255, 0), -1)
							sonido_impacto()
							print("EEEEN EL CLAVOOOOOOOO (1)")
						# En caso de que la pelo esta en la pantalla pero no este en el medio:
						# Se imprimira un 0 y lo rodea con un circulo rojo
						else :
							cv2.circle(frame, (int(x), int(y)), int(radius),(0, 0, 255), 2)
							cv2.circle(frame, center, 5, (0, 0, 255), -1)
							print("QUEEE MALA PUNTERIAAAAAAAAA (0)")

				# En caso de que se dispare pero no haya bola o parte de ella, se imprimira esto:
				else:

					print("La bola no esta ni en la camara!!!!!!!!!!")

						# CREO QUE ES IMPORTANTE ESPECIFICAR UNA COSA:
						# Cuando no se pulsa el boton del medio no veremos a la pelota verde rodeada
						# por un circulo rojo o un circulo verde, solo veremos las lineas azules de delimitacion
						# y la bola en si. Cuando se pulsa el boton del medio es cuando la bola (dependiendo de si ha sido detectado)
						# se rodeara de un circulo rojo o verde.

				##############################################################################
      			############# FIN CODIGO DE LA CAMARA CUANDO SE REALIZA EL DISPARO ###########
      			##############################################################################


		      		sense.show_letter("M")      # Enter key

	    # CUIDADO CON ESTE TIEMPO PORQUE TAMBIEN AFECTA A LA HORA
	    # DE CAPTURAR FRAMES POR SEGUNDO !!!!!!!!!!
	    	sleep(0.2)
	    	sense.clear()

	    # MIRAR A VER INDEXACIONES PORQUE NO SE SI EL SLEEP Y SENSE.CLEAR DEBERIAN ESTAR AQUI:
	    #sleep(0.2)
	    #sense.clear()

	    # O AQUI
	#sleep(0.2)
	#sense.clear()


	####################################################################
	######### CODIGO PARA MOSTRAR POR PANTALLA EL FRAME ################
	####################################################################


	# Muestra en la pantalla el frame capturado y modificado
	cv2.imshow("Frame", frame)
	key = cv2.waitKey(1) & 0xFF

	# Si se pulsa la q, se sale del bucle
	if key == ord("q"):
		break

	#####################################################################
	########## FIN CODIGO PARA MOSTRAR POR PANTALLA EL FRAME ###########
	#####################################################################

# Cuando se sale del bucle limpa la camara y cierra cualquier ventana
camera.release()
cv2.destroyAllWindows()

	     		









