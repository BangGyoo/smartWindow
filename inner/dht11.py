#!/usr/bin/python
import RPi.GPIO as GPIO
import Adafruit_DHT
import sys #  argv[1] is loop count
import time

sensor = Adafruit_DHT.DHT11

# GPIO23

pin = 4

humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)

loop = 0
average_h = 0.0
average_t = 0.0

while loop < int(sys.argv[1]) :
    if humidity is not None and temperature is not None:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        average_h += float(humidity)
        average_t += float(temperature)
    else:
        print "Failed to get reading."
    loop += 1
    
average_t = average_t / int(sys.argv[1])
average_h = average_h / int(sys.argv[1])

print("%10s%10s"%(average_t,average_h))
    
