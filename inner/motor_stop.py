import RPi.GPIO as GPIO
import time, sys
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

#GPIO.setup(23,GPIO.IN)

GPIO.output(19,False)
GPIO.output(26,False)


