import RPi.GPIO as GPIO
import time, sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

try :
    window_status = open("window_status.txt",'r')
    window = window_status.readline()
    window_status.close()

        

    window_status = open("window_status.txt",'w')
    
    if (sys.argv[1] == "cw" and window != "0") :
        GPIO.output(26, True)
        print("set motor on")
        print("set close")
        window_status.write("2")
        GPIO.output(19,True)

    elif (sys.argv[1] == "ccw" and window != "1") :
        GPIO.output(26, True)
        print("set motor on")
        window_status.write("2")
        print("set open")
        GPIO.output(19,False)
    else :
        sys.exit()

    window_status.close()
    time.sleep(0.5)

except KeyboardInterrupt :
    window_status = open("window_status.txt",'w')
    window_status.write("2")    
    sys.exit()
