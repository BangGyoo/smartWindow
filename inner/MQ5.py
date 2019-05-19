import time
import RPi.GPIO as GPIO
import sys # argv[1] is loop count

pin = 3
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

loop = 0
while loop < int(sys.argv[1]):
    if not(GPIO.input(pin)) :
        print('1')
        sys.exit()   
    loop += 1
print("0")

