import RPi.GPIO as GPIO
import sys
GPIO.setmode(GPIO.BCM)
GPIO.setup(18,GPIO.IN)


loop = 0
while loop < int(sys.argv[1]) :
	if not(GPIO.input(18)) :
		print("1")
		sys.close()
print("0")
