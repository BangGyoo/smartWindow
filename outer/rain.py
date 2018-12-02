import time
import RPi.GPIO as GPIO
import sys # argv[1] is loop count

pin = 7
GPIO.setmode(GPIO.BCM)
GPIO.setup(pin, GPIO.IN)

loop = 0
while loop < int(sys.argv[1]):
    if GPIO.input(pin):
        active_time = time.time()
        print("No Rain Detected")
        print(active_time)
        time.sleep(0.1)
    else:
        active_time = time.time()
        print("Rain Detected!")
        print(active_time)
        time.sleep(0.1)
    loop += 1
