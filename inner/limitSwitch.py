import RPi.GPIO as GPIO
import time, sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)

try :
    loop=0
    while loop < 5 :
        if ((GPIO.input(5))==False) or ((GPIO.input(6))==False) :
            window_status = open("window_status.txt",'w')
            if not(GPIO.input(5)) :
                window_status.write("1")
                print("open limit")
            else :
                window_status.write("0")
                print("close limit")
            GPIO.output(26,False)
            window_status.close()
            sys.exit()
        loop+=1

except KeyboardInterrupt :
    sys.exit()

