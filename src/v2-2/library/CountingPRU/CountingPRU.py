#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################################################
#
# Simples interface em Python 2 (através do modulo ctypes) para uso da biblioteca libCountingPRU.
#
####################################################################################################

if (__name__ == "__main__"):
    exit()

# Importa o modulo ctypes
import ctypes


# Carrega as bibliotecas dinâmicas das quais a biblioteca libCountingPRU depende (bibliotecas da
# PRU)
ctypes.CDLL("libprussdrv.so", mode = ctypes.RTLD_GLOBAL)
ctypes.CDLL("libprussdrvd.so", mode = ctypes.RTLD_GLOBAL)

# Carrega a biblioteca libCountingPRU
libCountingPRU = ctypes.CDLL("libCountingPRU.so", mode = ctypes.RTLD_GLOBAL)

# Buffer para contadores
count_buffer = (ctypes.c_uint32 * 8)()


# Procedimento de inicializacao da PRU
def Init():
    libCountingPRU.init_start_PRU()


# Aciona contagem
def Counting(time_base):
    libCountingPRU.Counting(ctypes.c_float(time_base), ctypes.byref(count_buffer))
    answer = []
    for i in range (8):
        answer.append(count_buffer[i])
    return answer



# Encerra a PRU
def Close():
    libCountingPRU.close_PRU()
