#!/usr/bin/env python-sirius
# -*- coding: utf-8 -*-
import sys
import os
import traceback
import time
import datetime
import socket
import struct
from threading import Event, Thread
import Adafruit_BBIO.GPIO as GPIO
import CountingPRU
import redis

# Variable for timebase counting and Serial Numbers
global TimeBase, SerialNumber
BSMP_ID_SERIALNUMBER_CHANNEL = {
    11: '1', 12: '2', 13: '3', 14: '4', 15: '5', 16: '6', 17: '7', 18: '8'}

# Connect to Redis DB
redis_db = redis.StrictRedis(host='127.0.0.1', port=6379)


# Get value from Redis key. If does not exist, create it.
if not redis_db.exists("TimeBase"):
    sys.stdout.write("Creating TimeBase variable\n")
    sys.stdout.flush()
    redis_db.set("TimeBase", 60)
    redis_db.save()

# If TimeBase is zero, set it to a different value
if float(redis_db.get("TimeBase")) == 0:
    sys.stdout.write("TimeBase was zero. Set it to a reasonable value: 60.\n")
    sys.stdout.flush()
    redis_db.set("TimeBase", 60)
    redis_db.save()


TimeBase = float(redis_db.get("TimeBase"))


# Get Serial Numbers from Redis DB
for channel in list(BSMP_ID_SERIALNUMBER_CHANNEL.keys()):
    if not redis_db.hexists('DetectorSerialNumber', BSMP_ID_SERIALNUMBER_CHANNEL[channel]):
        redis_db.hset('DetectorSerialNumber',
                      BSMP_ID_SERIALNUMBER_CHANNEL[channel], 0)


# Variable for counting values [LNLS1, LNLS2, LNLS3, LNLS4, LNLS5, LNLS6, Bergoz1, Bergoz2]
global Counting
Counting = [0]*8

# Inhibit pins - Bergoz
Inhibit = {"A1": "P9_14", "B1": "P9_16", "A2": "P9_13", "B2": "P9_15"}

for pin in Inhibit:
    GPIO.setup(Inhibit[pin], GPIO.OUT)
    GPIO.output(Inhibit[pin], GPIO.LOW)


# Error Codes - bsmp
COMMAND_OK = 0xE0
ERROR_READ_ONLY = 0xE6


# Datetime string
def time_string():
    return(datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S.%f")[:-4] + " - ")


def includeChecksum(list_values):
    counter = 0
    i = 0
    while (i < len(list_values)):
        counter += list_values[i]
        i += 1
    counter = (counter & 0xFF)
    counter = (256 - counter) & 0xFF
    return list_values + [counter]


def verifyChecksum(list_values):
    counter = 0
    i = 0
    while (i < len(list_values)):
        counter += list_values[i]
        i += 1
    counter = (counter & 0xFF)
    return(counter)


def sendVariable(variableID, value, size):
    send_message = [0x00, 0x11] + [ord(c) for c in struct.pack("!h", size)]
    if size == 1:
        send_message = send_message + [value]
    elif size == 2:
        send_message = send_message + [ord(c)
                                       for c in struct.pack("!h", value)]
    elif size == 4:
        send_message = send_message + [ord(c)
                                       for c in struct.pack("!I", value)]
    return "".join(map(chr, includeChecksum(send_message)))


def sendGroup(GroupID, values, size):
    send_message = [0x00, 0x13] + [ord(c) for c in struct.pack("!h", size)]
    size_var = size / len(values)
    if size_var == 2:
        for value in values:
            send_message = send_message + \
                [ord(c) for c in struct.pack("!h", value)]
    elif size_var == 4:
        for value in values:
            send_message = send_message + \
                [ord(c) for c in struct.pack("!I", value)]
    return "".join(map(chr, includeChecksum(send_message)))


def sendMessage(ErrorCode):
    return "".join(map(chr, includeChecksum([0x00, ErrorCode, 0x00, 0x00])))


# Thead to send and receive values on demand
class Communication(Thread):
    def __init__(self, port):
        Thread.__init__(self)
        self.port = port

    def run(self):
        global TimeBase, Counting
        while (True):
            try:

                # TCP/IP socket initialization
                self.tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.tcp.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                self.tcp.bind(("", self.port))
                self.tcp.listen(1)
                sys.stdout.write(
                    time_string() + "TCP/IP Server on port " + str(self.port) + " started.\n")
                sys.stdout.write(
                    time_string() + "Timebase: {}.\n".format(TimeBase))
                sys.stdout.flush()

                while (True):

                    sys.stdout.write(
                        time_string() + "Waiting for connection.\n")
                    sys.stdout.flush()
                    con, client_info = self.tcp.accept()

                    # New connection
                    sys.stdout.write(time_string() + "Connection accepted from " +
                                     client_info[0] + ":" + str(client_info[1]) + ".\n")
                    sys.stdout.flush()

                    while (True):
                        # Get message
                        message = [ord(i) for i in con.recv(100)]
                        if(message):
                            if (verifyChecksum(message) == 0):

                                # Variable Read
                                if message[1] == 0x10:
                                    # TimeBase
                                    if message[4] == 0x00:
                                        con.send(sendVariable(
                                            message[4], TimeBase, 2))
                                    elif message[4] <= 0x08:
                                        con.send(sendVariable(
                                            message[4], Counting[message[4]-1], 4))

                                    # Inhibit pins - 8 bits: X X X X B2 A2 B1 A1
                                    elif message[4] == 0x09:
                                        inh_value = 0
                                        for i in range(4):
                                            inh_value += GPIO.input(
                                                Inhibit[list(Inhibit.keys())[i]]) * (2**i)
                                        con.send(sendVariable(
                                            message[4], inh_value, 1))

                                    # SerialNumbers
                                    elif message[4] >= 11 and message[4] <= 18:
                                        con.send(sendVariable(message[4], int(redis_db.hget(
                                            "DetectorSerialNumber", BSMP_ID_SERIALNUMBER_CHANNEL[message[4]])), 1))

                                # Group Read
                                elif message[1] == 0x12:
                                    if message[4] == 0x01:
                                        con.send(
                                            sendGroup(message[4], Counting, len(Counting)*4))

                                # Variable Write
                                elif message[1] == 0x20:
                                    # TimeBase
                                    if message[4] == 0x00:
                                        TimeBase = message[5]*256 + message[6]
                                        redis_db.set("TimeBase", TimeBase)
                                        try:
                                            redis_db.save()
                                        except:
                                            pass
                                        con.send(sendMessage(COMMAND_OK))
                                        sys.stdout.write(
                                            time_string() + "Write time base " + str(TimeBase) + " \n")
                                        sys.stdout.flush()
                                    # Counting channels
                                    elif message[4] <= 0x08:
                                        con.send(sendMessage(ERROR_READ_ONLY))
                                    # Inhibit pins - 8 bits: X X X X B2 A2 B1 A1
                                    elif message[4] == 0x09:
                                        for i in range(4):
                                            GPIO.output(Inhibit[list(Inhibit.keys())[
                                                        i]], bool(message[5] & (1 << i)))
                                        con.send(sendMessage(COMMAND_OK))
                                        sys.stdout.write(
                                            time_string() + "Write Inhibits to " + bin(message[5] & 0x0f) + " \n")
                                        sys.stdout.flush()

                                    # SerialNumbers
                                    elif message[4] >= 11 and message[4] <= 18:
                                        redis_db.hset(
                                            "DetectorSerialNumber", BSMP_ID_SERIALNUMBER_CHANNEL[message[4]], message[5])
                                        try:
                                            redis_db.save()
                                        except:
                                            pass
                                        con.send(sendMessage(COMMAND_OK))
                                        sys.stdout.write(time_string() + "Write SN {} to device attached to ch {}\n".format(
                                            message[5], BSMP_ID_SERIALNUMBER_CHANNEL[message[4]]))
                                        sys.stdout.flush()

                            else:
                                sys.stdout.write(
                                    time_string() + "Unknown message\n")
                                sys.stdout.flush()
                                continue

                        else:
                            # Disconnection
                            sys.stdout.write(time_string(
                            ) + "Client " + client_info[0] + ":" + str(client_info[1]) + " disconnected.\n")
                            sys.stdout.flush()
                            break

            except Exception:
                self.tcp.close()
                sys.stdout.write(
                    time_string() + "Connection problem. TCP/IP server was closed. Error:\n\n")
                traceback.print_exc(file=sys.stdout)
                sys.stdout.write("\n")
                sys.stdout.flush()
                time.sleep(5)


# --------------------- MAIN LOOP ---------------------
# -------------------- starts here --------------------

# Initialize CountingPRU
CountingPRU.Init()


# Socket thread
net = Communication(5000)
net.daemon = True
net.start()


# Main loop - Counting Values!
# Counting list stores countings/second, multiplied by 1000
while 1:
    CurrentTimeBase = TimeBase
    Counting = [1000*value/float(CurrentTimeBase)
                for value in CountingPRU.Counting(CurrentTimeBase)]
