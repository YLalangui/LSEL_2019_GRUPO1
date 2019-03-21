from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
sense = SenseHat()

# Librerias a importar para hacer uso de la camara
from collections import deque
import numpy as np
import argparse
import imutils
import cv2

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
# verde que quiero que identifique. Además inicializa los puntos a trackear
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

def arriba():
	global valor_1
	
	if valor_1<999:
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+") 
		valor_1+=paso
		print(valor_1)
		print("arriba")
		duty.write(str(valor_1))
		duty.close()

	

def abajo():
	global valor_1
	if valor_1>500:
		duty = open("/sys/class/lse-pwm/pwm/duty", "rw+")
		valor_1-=paso
		print(valor_1)
		print("abajo")
		duty.write(str(valor_1))
		duty.close()
def derecha():
	global valor_2
	if valor_2<999:
		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2+=paso
		print(valor_2)
		print("derecha")
		duty.write(str(valor_2))
		duty.close()

def izquierda():
	global valor_2
	if valor_2>500:
		duty = open("/sys/class/lse-pwm_2/pwm/duty", "rw+") 
		valor_2-=paso
		print(valor_2)
		print("izquierda")
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
	# Si el sleep es mas pequeño pues habra mas frames por segundo
	(grabbed, frame) = camera.read()

	# Si se esta viendo el video pero no se coge ningun frame significara
	# que el video ha terminado
	if args.get("video") and not grabbed:
		break

	# Para los mas curiosos: Pilla el frame y le hace pasar por un filtro
	# que emborrona la imagen para faciliar su procesado. Luego lo hace
	# pasar al espacio de color hsv (en vez de rgb) -> No todo es RGB eh?
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

	     		






































