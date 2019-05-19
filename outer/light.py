import RPi.GPIO as GPIO
import sys
import time
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN)


loop = 0
while loop < int(sys.argv[1]) :
	if (GPIO.input(18)) :
		print("1")
		sys.exit()
	else :
		print(GPIO.input(18))
	loop+=1
	time.sleep(0.1)
