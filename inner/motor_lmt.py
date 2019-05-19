import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#GPIO.setup(23,GPIO.IN)

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
    time.sleep(1)
    while(1) :
        if ((GPIO.input(5))==False) or ((GPIO.input(6))==False) :
            print("%5s, %5s"%(GPIO.input(5),bool(GPIO.input(5))))
            print("limit!!")
            sys.exit()
        time.sleep(0.1)
finally :
    GPIO.output(26,False)
    GPIO.output(19,False)
    sys.exit()
