import RPi.GPIO as GPIO
import time, sys


GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)

try :
        time.sleep(0.1)
        if ((GPIO.input(5))==False) or ((GPIO.input(6))==False) :
            window_status = open("window_status.txt",'w')
            if not(GPIO.input(5)) :
               window_status.write("1")
               GPIO.output(26,False)
               window_status.close()
               print("open limit")
               time.sleep(0.7)
            else :
               window_status.write("0")
               GPIO.output(26,False)
               window_status.close()
               print("close limit")
               time.sleep(0.7)
            sys.exit()

except KeyboardInterrupt :
    sys.exit()

