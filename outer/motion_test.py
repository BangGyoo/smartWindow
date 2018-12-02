import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
pin = 23
GPIO.setup(pin, GPIO.IN)
print "Waiting for sensor to settle"
print "Detecting motion"
while True:
    if GPIO.input(pin):
        print "On"
    else :
        print "None"
    time.sleep(2)
