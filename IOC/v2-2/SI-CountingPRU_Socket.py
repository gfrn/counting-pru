#!/usr/bin/env python
# -*- coding: utf-8 -*-

import sys, os, traceback
import time, datetime
import socket, struct
from threading import Event, Thread
import Adafruit_BBIO.GPIO as GPIO
import CountingPRU


# Variable for timebase counting
global TimeBase
TimeBase = 1

# Variable for counting values [LNLS1, LNLS2, LNLS3, LNLS4, LNLS5, LNLS6, Bergoz1, Bergoz2]
global Counting

# Inhibit pins - Bergoz
Inhibit = {"A1":"P9_14", "B1":"P9_16", "A2":"P9_13", "B2":"P9_15"}

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
    send_message = [0x00, 0x11] + [ord(c) for c in struct.pack("!h",size+1)] + [variableID]
    if size == 2:
        send_message = send_message + [ord(c) for c in struct.pack("!h",value)]
    elif size == 4:
        send_message = send_message + [ord(c) for c in struct.pack("!I",value)]
    return "".join(map(chr,includeChecksum(send_message)))

def sendMessage(ErrorCode):
    return "".join(map(chr,includeChecksum([0x00, ErrorCode, 0x00, 0x00])))


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
                sys.stdout.write(time_string() + "TCP/IP Server on port " + str(self.port) + " started.\n")
                sys.stdout.flush()

                while (True):

                    sys.stdout.write(time_string() + "Waiting for connection.\n")
                    sys.stdout.flush()
                    con, client_info = self.tcp.accept()

                    # New connection
                    sys.stdout.write(time_string() + "Connection accepted from " + client_info[0] + ":" + str(client_info[1]) + ".\n")
                    sys.stdout.flush()

                    while (True):
                        # Get message
                        message = [ord(i) for i in con.recv(100)]
                        if(message):
                            if (verifyChecksum(message)==0):

                                # Command Read
                                if message[1] == 0x10:
                                    if message[4] < 0x08:
                                        con.send(sendVariable(message[4], Counting[message[4]], 4))
                                        sys.stdout.write(time_string() + "Read counting " + str(message[4]) + " \n")
                                        sys.stdout.flush()
                                    # TimeBase
                                    elif message[4] == 0x08:
                                        con.send(sendVariable(message[4], TimeBase, 2))
                                        sys.stdout.write(time_string() + "Read time base " + str(TimeBase) + " \n")
                                        sys.stdout.flush()
                                    # Inhibit pins - 8 bits: X X X X B2 A2 B1 A1
                                    elif message[4] == 0x09:
                                        inh_value = 0
                                        for i in range (4):
                                            inh_value += GPIO.input(Inhibit[Inhibit.keys()[i]]) * (2**i)
                                            con.send(sendVariable(message[4], inh_value, 1))
                                            sys.stdout.write(time_string() + "Read Inhibits values " + bin(inh_value) + " \n")
                                            sys.stdout.flush()


                                # Command Write
                                elif message[1] == 0x20:
                                    # Counting channels
                                    if message[4] < 0x08:
                                        con.send(sendMessage(ERROR_READ_ONLY))
                                        sys.stdout.write(time_string() + "Write to counting " + str(message[4]) + " not permited.\n")
                                        sys.stdout.flush()
                                    # TimeBase
                                    elif message[4] == 0x08:
                                        TimeBase = message[5]*256 + message[6]
                                        con.send(sendMessage(COMMAND_OK))
                                        sys.stdout.write(time_string() + "Write time base " + str(TimeBase) + " \n")
                                        sys.stdout.flush()
                                    # Inhibit pins - 8 bits: X X X X B2 A2 B1 A1
                                    elif message[4] == 0x09:
                                        for i in range (4):
                                            GPIO.output(Inhibit[Inhibit.keys()[i]], bool(message[5] & (1 << i)))
                                            con.send(sendMessage(COMMAND_OK))
                                            sys.stdout.write(time_string() + "Write Inhibits to " + bin(message[5]&0x0f) + " \n")
                                            sys.stdout.flush()



                            else:
                                sys.stdout.write(time_string() + "Unknown message\n")
                                sys.stdout.flush()
                                continue

                        else:
                            # Disconnection
                            sys.stdout.write(time_string() + "Client " + client_info[0] + ":" + str(client_info[1]) + " disconnected.\n")
                            sys.stdout.flush()
                            break


            except Exception:
                self.tcp.close()
                sys.stdout.write(time_string() + "Connection problem. TCP/IP server was closed. Error:\n\n")
                traceback.print_exc(file = sys.stdout)
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
while 1:
    Counting = CountingPRU.Counting(TimeBase)
