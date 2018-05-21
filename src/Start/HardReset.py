#!/usr/bin/python

import Adafruit_BBIO.GPIO as gpio
import time


gpio.setup("P9_11", gpio.OUT)

while(1):
        gpio.output("P9_11", gpio.LOW)
        gpio.output("P9_11", gpio.HIGH)
        time.sleep(5)


