import RPi.GPIO as GPIO # argv[1] is cw / ccw flag , full speed 23sec
import time       # argv[2] is open time
import sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(19, GPIO.OUT)
GPIO.setup(26, GPIO.OUT)

if sys.argv[1] == "cw" :
    print ("set motor on")
    GPIO.output(26, True)
    print ("set motor cw")
    GPIO.output(19, False)
    time.sleep(float(sys.argv[2]))
    print ("set motor off")
    GPIO.output(26,False)

    
elif sys.argv[1] == "ccw" :
    print ("set motor on")
    GPIO.output(26,True)
    print ("set motor ccw")
    GPIO.output(19, True)
    print ("set motor off")
    time.sleep(float(sys.argv[2]))
    GPIO.output(26,False)
                
else :
    print("input value error")

GPIO.cleanup()
