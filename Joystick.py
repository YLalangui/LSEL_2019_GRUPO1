from sense_hat import SenseHat, ACTION_PRESSED, ACTION_HELD, ACTION_RELEASED
from time import sleep
sense = SenseHat()

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
        		sense.show_letter("M")      # Enter key
			
      
      		# Wait a while and then clear the screen
     		sleep(1)
     		sense.clear()
