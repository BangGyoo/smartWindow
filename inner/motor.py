import RPi.GPIO as GPIO
import time, sys
import threading
import subprocess

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)

def LimitSwitch() :
    subprocess.check_output("python3 ./limitSwitch.py",shell=True)

try :
    window_status = open("window_status.txt",'r')
    window = window_status.readline()
    window_status.close()

    
    if (sys.argv[1] == "cw" and window != "0") :
        GPIO.output(26, True)
        window_status = open("window_status.txt",'w')
        print("set motor on")
        print("set close")
        window_status.write("2")
        GPIO.output(19,True)
        window_status.close()

    elif (sys.argv[1] == "ccw" and window != "1") :
        GPIO.output(26, True)
        window_status = open("window_status.txt",'w')
        print("set motor on")
        window_status.write("2")
        print("set open")
        GPIO.output(19,False)
        window_status.close()
    time.sleep(0.5)
    #thread = threading.Thread(target=LimitSwitch,args=())
    #thread.start()

except KeyboardInterrupt :
    GPIO.output(26,False)
    sys.exit()
