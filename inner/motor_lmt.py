import RPi.GPIO as GPIO
import time, sys
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(5,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#GPIO.setup(23,GPIO.IN)

def limitSwitch() :
     while(1) :
        if ((GPIO.input(5))==False) or ((GPIO.input(6))==False) :
            
            window_status = open("window_status.txt",'w')
            if not(GPIO.input(5)) :
                window_status.write("1")
            else :
                window_status.write("0")
            window_status.close()
            GPIO.output(26,False)
            GPIO.output(19,False)
            print("%5s, %5s"%(GPIO.input(5),bool(GPIO.input(6))))
            print("limit!!")
            sys.exit()
        time.sleep(0.1)
   

try :
    window_status = open("window_status.txt",'r')
    window = window_status.readline()
    
    GPIO.output(26, True)
    print("set motor on")

    if sys.argv[1] == "cw" and window != "0" :
        print("set motor cw")
        GPIO.output(19, True)
    elif sys.argv[1] == "ccw" and window != "1" :
        print("set motor ccw")
        GPIO.output(19,False)
    else :
        sys.exit()
    thread = threading.Thread(target=limitSwitch,args=())
    thread.start()
    #time.sleep(1)
except KeyboardInterrupt :
    window_status = open("window_status.txt",'w')
    window_status.write("2")
    sys.exit()
finally :
    GPIO.output(26,False)
    GPIO.output(19,False)
 
