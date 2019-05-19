import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN)

try :
    
    GPIO.output(26, True)
    print("set motor on")

    if sys.argv[1] == "cw" :
        print("set motor cw")
        GPIO.output(19, True)
    elif sys.argv[1] == "ccw" :
        print("set motor ccw")
        GPIO.output(19,False)
    else :
        print("input value error")
    while(1) :
        if GPIO.input(6) :
            print("limit!!")
            sys.exit()
            
finally :
    GPIO.output(26,False)
    GPIO.output(19,False)
    sys.exit()
