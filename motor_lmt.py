import RPi.GPIO as GPIO
import time, sys

GPIO.setmode(GPIO.BCM)
GPIO.setup(19,GPIO.OUT)
GPIO.setup(26,GPIO.OUT)
GPIO.setup(6,GPIO.IN,pull_up_down=GPIO.PUD_UP)
GPIO.setup(23,GPIO.IN,pull_up_down=GPIO.PUD_UP)

#GPIO.setup(23,GPIO.IN)

try :
    
    GPIO.output(26, True)
    print("set motor on")

    if sys.argv[1] == "cw" :
        print("set motor cw")
        GPIO.output(19, True)
    elif sys.argv[1] == "ccw" :
        print("set motor ccw")
        GPIO.output(19,False)
    else :
        print("input value error")
    loop23 = 0
    loop6  = 0
    time.sleep(1)
    while(1) :
        if bool(GPIO.input(23))==False :
            loop23 +=1
            print("23=%s"%loop23)
        if GPIO.input(6)==False :
            loop6  +=1
            print("6=%s"%loop6)
        if loop6 > 3 or loop23 > 3:
            print("%5s, %5s"%(GPIO.input(23),bool(GPIO.input(23))))
            print("limit!!")
            sys.exit()
        time.sleep(0.1)
finally :
    GPIO.output(26,False)
    GPIO.output(19,False)
    sys.exit()
