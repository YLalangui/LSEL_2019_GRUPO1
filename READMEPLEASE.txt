Hola chavales, bienvenidos a una introducci�n a Ingenier�a del Software.
Cuando una persona hace un cambio en un c�digo o es necesario seguir unos pasos para ejecutar su c�digo
es de agradecer que cree un README para futuros usuarios, y es lo que voy a hacer aqu�.

Para que se pueda hacer uso de la c�mara es necesario usar el entorno virtual es la raspberry e inicial una sesi�n X con la raspberry
Esto se ejecuta en un terminal del ordenador:

alumno@alumno$ ssh -X pi@{Direccion IP}

En este momento ya estaremos en la raspberry y se tendr� que iniciar el entorno virtual:

pi@loquesea$ source /home/pi/.profile
pi@loquesea$ workon cv

Ahora se ver� que el indicador habr� cambiado a algo como esto:

(cv) pi@loquesea$

Lo que significar� que estaremos dentro del entorno virtual.

A partir de este momento ya se pueede ejecutar el Joystick.py y ver como sale la pantalla mostrando lo que se ve
en la c�mara.

En principio as� de primeras no tendr�a que haber ning�n error, pero si sale algo me avis�is, me dec�s cu�l es el problema y
lo veo desde el trabajo xD.