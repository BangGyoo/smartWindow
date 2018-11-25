import RPi.GPIO as GPIO

import time

GPIO.setmode(GPIO.BCM)
GPIO.setup(23,GPIO.OUT)
GPIO.setup(7,GPIO.OUT)
GPIO.setup(18,GPIO.OUT)
GPIO.setup(21,GPIO.OUT)
GPIO.setup(2,GPIO.OUT)
GPIO.setup(3,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(4,GPIO.OUT)

print("testing out, Press CTRL+c to exit")

try :
    while True :
        print("set GPIO high")
        GPIO.output(23,True)
        GPIO.output(7,True)
        GPIO.output(18,True)
        GPIO.output(21,True)
        GPIO.output(2,True)
        GPIO.output(3,True)
        GPIO.output(26,True)
        GPIO.output(19,True)    
        GPIO.output(13,True)
        GPIO.output(4,True)
        time.sleep(2)
        GPIO.output(23,False)
        GPIO.output(7,False)
        GPIO.output(18,False)
        GPIO.output(21,False)
        GPIO.output(2,False)
        GPIO.output(3,False)
        GPIO.output(26,False)
        GPIO.output(19,False)
        GPIO.output(13,False)
        GPIO.output(4,False)
        time.sleep(2)
except KeyboardInterrupt :
    print("Keyborad interrupt")
except :
    print("some error")
finally:
    print("clean up")
    GPIO.cleanup()
