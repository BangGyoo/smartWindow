import RPi.GPIO as GPIO
import time 

out1 = 13
out2 = 15
out3 = 11
out4 = 12

i=0
positive=0
negative=0
y=0

def turnoff() :
      time.sleep(0.001)
#      GPIO.output(out1,GPIO.LOW)
#      GPIO.output(out2,GPIO.LOW)
#      GPIO.output(out3,GPIO.LOW)
#      GPIO.output(out4,GPIO.LOW)
    

GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

try:
   
   while(1):
      turnoff()      

      GPIO.output(out1,GPIO.HIGH)
      GPIO.output(out2,GPIO.LOW)
      GPIO.output(out3,GPIO.LOW)
      GPIO.output(out4,GPIO.LOW)
          
      turnoff()      
      GPIO.output(out1,GPIO.HIGH)
      GPIO.output(out2,GPIO.HIGH)
      GPIO.output(out3,GPIO.LOW)
      GPIO.output(out4,GPIO.LOW)
      
      turnoff()      
      GPIO.output(out1,GPIO.LOW)
      GPIO.output(out2,GPIO.HIGH)
      GPIO.output(out3,GPIO.LOW)
      GPIO.output(out4,GPIO.LOW)

      turnoff()      
      GPIO.output(out1,GPIO.LOW)
      GPIO.output(out2,GPIO.HIGH)
      GPIO.output(out3,GPIO.HIGH)
      GPIO.output(out4,GPIO.LOW)
      turnoff()      
      GPIO.output(out1,GPIO.LOW)
      GPIO.output(out2,GPIO.LOW)
      GPIO.output(out3,GPIO.HIGH)
      GPIO.output(out4,GPIO.LOW)
 
      turnoff()      
      GPIO.output(out1,GPIO.LOW)
      GPIO.output(out2,GPIO.LOW)
      GPIO.output(out3,GPIO.HIGH)
      GPIO.output(out4,GPIO.HIGH)
      
      turnoff()      
      GPIO.output(out1,GPIO.LOW)
      GPIO.output(out2,GPIO.LOW)
      GPIO.output(out3,GPIO.LOW)
      GPIO.output(out4,GPIO.HIGH)

      turnoff()      
      GPIO.output(out1,GPIO.HIGH)
      GPIO.output(out2,GPIO.LOW)
      GPIO.output(out3,GPIO.LOW)
      GPIO.output(out4,GPIO.HIGH)
      
          
except KeyboardInterrupt:
    GPIO.cleanup()
