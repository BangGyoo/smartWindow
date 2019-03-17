import RPi.GPIO as GPIO
import time
import sys

GPIO.setmode(GPIO.BCM)
pin = 21
GPIO.setup(pin, GPIO.IN)
print "Waiting for sensor to settle"
print "Detecting motion"
loop = 0
while loop < int(sys.argv[1]) :
    if GPIO.input(pin):
        print "0"
    else :
        print "1"
    time.sleep(0.01)
    loop+=1
