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

while loop < int(sys.argv[1]) :
    if humidity is not None and temperature is not None:
        humidity, temperature = Adafruit_DHT.read_retry(sensor, pin)
        print "Temp={0:0.1f}*C Humidity={1:0.1f}%".format(temperature, humidity)
        time.sleep(0.1)
    else:
        print "Failed to get reading."
    loop += 1
    
