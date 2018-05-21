#!/usr/bin/python

import Adafruit_BBIO.GPIO as GPIO
import time

GPIO.setup("P8_8", GPIO.OUT)

while True:
        GPIO.output("P8_8", GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output("P8_8", GPIO.LOW)
        time.sleep(0.1)
        GPIO.output("P8_8", GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output("P8_8", GPIO.LOW)
        time.sleep(1)


