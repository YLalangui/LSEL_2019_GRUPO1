Hola chavales, bienvenidos a una introducción a Ingeniería del Software.
Cuando una persona hace un cambio en un código o es necesario seguir unos pasos para ejecutar su código
es de agradecer que cree un README para futuros usuarios, y es lo que voy a hacer aquí.

Para que se pueda hacer uso de la cámara es necesario usar el entorno virtual es la raspberry e inicial una sesión X con la raspberry
Esto se ejecuta en un terminal del ordenador:

alumno@alumno$ ssh -X pi@{Direccion IP}

En este momento ya estaremos en la raspberry y se tendrá que iniciar el entorno virtual:

pi@loquesea$ source /home/pi/.profile
pi@loquesea$ workon cv

Ahora se verá que el indicador habrá cambiado a algo como esto:

(cv) pi@loquesea$

Lo que significará que estaremos dentro del entorno virtual.

A partir de este momento ya se pueede ejecutar el Joystick.py y ver como sale la pantalla mostrando lo que se ve
en la cámara.

En principio así de primeras no tendría que haber ningún error, pero si sale algo me avisáis, me decís cuál es el problema y
lo veo desde el trabajo xD.