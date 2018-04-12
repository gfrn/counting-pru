#!/usr/bin/python
# -*- coding: utf-8 -*-

'''
CountingPRU.py
v2-2

--------------------------------------------------------------------------------
PRU-based Counters
--------------------------------------------------------------------------------
Interfaces with CountingPRU Hardware (v2-2) in order to count trains of pulses
either from Bergoz Differential BLM or from LNLS Gamma Sensors (4-channel
standard TTL signal)

*** Python2 interface (using ctypes module) for using libCountingPRU library ***

Brazilian Synchrotron Light Laboratory (LNLS/CNPEM)
Controls Group

Author: Patricia HENRIQUES NALLIN
Date: March/2018
'''

if (__name__ == "__main__"):
    exit()

# ----- Import
import ctypes


# ----- Import dependancy libraries
ctypes.CDLL("libprussdrv.so", mode = ctypes.RTLD_GLOBAL)
ctypes.CDLL("libprussdrvd.so", mode = ctypes.RTLD_GLOBAL)


# ----- Import libCountingPRU
libCountingPRU = ctypes.CDLL("libCountingPRU.so", mode = ctypes.RTLD_GLOBAL)


# ----- Buffer for counter values
count_buffer = (ctypes.c_uint32 * 8)()




# ----- PRU INITIALIZATION
def Init():
    libCountingPRU.init_start_PRU()


# ----- COUNTING PULSES
# time_base: counting time base, in seconds
def Counting(time_base):
    libCountingPRU.Counting(ctypes.c_float(time_base), ctypes.byref(count_buffer))
    answer = []
    for i in range (8):
        answer.append(count_buffer[i])
    return answer


# ----- CLOSING PRU
def Close():
    libCountingPRU.close_PRU()
