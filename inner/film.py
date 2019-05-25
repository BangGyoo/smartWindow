import RPi.GPIO as GPIO # argv[1] is flim on/off
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(13, GPIO.OUT) 
GPIO.setwarnings(False)


if sys.argv[1] == "on" :
    print ("Film On")
    GPIO.output(13, True)
elif sys.argv[1] == "off" :
    print ("Flim Off")
    GPIO.output(13, False)

else :
    print("input value error")
