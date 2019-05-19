import RPi.GPIO as GPIO # argv[1] is cw / ccw flag , full speed 23sec
import time     
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)
limitSwitch = 6
GPIO.setup(limitSwitch,  GPIO.IN,pull_up_down=GPIO.PUD_DOWN)

def action(pin) :
    print("stop")  
    GPIO.output(26,False)
    GPIO.output(19,False)           
    GPIO.cleanup()
    sys.exit()

if sys.argv[1] == "cw" :
    print ("set motor on")
    GPIO.output(26, True)
    print ("set motor cw")
    GPIO.output(19, True)
elif sys.argv[1] == "ccw" :
    print ("set motor on")
    GPIO.output(26,True)
    print ("set motor ccw")
    GPIO.output(19, False)
time.sleep(1)
try :
    while(True) :
        print("move")
        if GPIO.input(limitSwitch) :
            action(limitSwitch)

except KeyboardInterrupt :
    GPIO.output(26,False)
    GPIO.output(19,False)
    GPIO.cleanup()
    sys.exit()
