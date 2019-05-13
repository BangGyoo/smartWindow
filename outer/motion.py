import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
pin = 21
GPIO.setup(pin, GPIO.IN)
loop = 0
while loop < int(sys.argv[1]) :
    if not(GPIO.input(pin)):
        print "0"
        sys.close()
    loop+=1
print "1"

