insmod /home/pi/Desktop/lse_pwm_2.ko
insmod /home/pi/Desktop/lse_pwm_3.ko

chmod -R 777  /sys/class/lse-pwm
chmod -R 777  /sys/class/lse-pwm_2
chmod -R 777  /sys/class/lse-pwm/pwm
chmod -R 777  /sys/class/lse-pwm_2/pwm
