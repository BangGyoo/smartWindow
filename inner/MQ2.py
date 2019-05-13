import RPi.GPIO as GPIO # argv[1] is searching count
import time, sys

GPIO.setmode(GPIO.BCM)

GPIO.setup(2, GPIO.IN , pull_up_down=GPIO.PUD_DOWN)

def action(pin) :
    print ("1")
    sys.exit()
    return

GPIO.add_event_detect(2, GPIO.RISING)
GPIO.add_event_callback(2, action)

try :
    loop = 0
    while loop < int(sys.argv[1]):
        loop += 1
    print("0")
    sys.exit()

except KeyboardInterrupt :
    sys.exit()
