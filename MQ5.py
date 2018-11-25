import RPi.GPIO as GPIO # argv[1] is searching count
import time, sys

GPIO.setmode(GPIO.BCM)

GPIO.setup(3, GPIO.IN , pull_up_down=GPIO.PUD_DOWN)

def action(pin) :
    print ("MQ5 error")
    return

GPIO.add_event_detect(3, GPIO.RISING)
GPIO.add_event_callback(3, action)

try :
    loop = 0
    while loop < int(sys.argv[1]):
        print('alive')
        time.sleep(0.5)
        loop += 1
    sys.exit()

except KeyboardInterrupt :
    sys.exit()
