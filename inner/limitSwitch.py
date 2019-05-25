import RPi.GPIO as GPIO
import time, sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)

try :
    while(1) :
        if ((GPIO.input(5))==False) or ((GPIO.input(6))==False) :
            window_status = open("window_status.txt",'w')
            if not(GPIO.input(5)) :
                window_status.write("1")
                print("open limit")
            else :
                window_status.write("0")
                print("close limit")
            window_status.close()
            GPIO.output(26,False)
            sys.exit()

except KeyboardInterrupt :
    window_status = open("window_status.txt",'w')
    window_status.write("2")
    window_status.close()
    sys.exit()
finally :
    GPIO.output(26,False)

