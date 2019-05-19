import RPi.GPIO as GPIO # argv[1] is on/off flag
import subprocess
import os,sys

x = 0
GPIO.setmode(GPIO.BCM)
GPIO.setup(26, GPIO.OUT)
try :
    if sys.argv[1] == "on" :
        print ("set motor on")
        GPIO.output(26, False)
    
    elif sys.argv[1] == "off" :
        print ("set motor off")
        GPIO.output(26,True)
    
    else :
        print("input value error")
    while(1) :
       x = int(subprocess.check_output("python ./limit.py",shell=True))
       print("result = %s"%x)
       if x == 1 :
           GPIO.output(26,False)
           sys.exit()
            
except KeyboardInterrupt :
    GPIO.output(26,False)
    sys.exit()
