import RPi.GPIO as GPIO # argv[1] is searching count
import os,time, sys

GPIO.setmode(GPIO.BCM)

GPIO.setup(6, GPIO.IN , pull_up_down=GPIO.PUD_DOWN)

def action(pin) :
    print ("1")
    sys.exit()
    return

GPIO.add_event_detect(6, GPIO.RISING)
GPIO.add_event_callback(6, action)

try :
    time.sleep(0.1)
    print("0")

except KeyboardInterrupt :
    sys.exit()
