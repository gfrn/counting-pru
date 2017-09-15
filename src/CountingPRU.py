#!/usr/bin/python
# -*- coding: utf-8 -*-

####################################################################################################
#
# Simples interface em Python 2 (através do modulo ctypes) para uso da biblioteca libReflexao.
#
####################################################################################################

# Este arquivo é um módulo Python, e não deve ser executado
if (__name__ == "__main__"):
    exit()

# Importa o modulo ctypes
import ctypes


# Carrega as bibliotecas dinâmicas das quais a biblioteca libPRUserial485 depende (bibliotecas da
# PRU)
ctypes.CDLL("libprussdrv.so", mode = ctypes.RTLD_GLOBAL)
ctypes.CDLL("libprussdrvd.so", mode = ctypes.RTLD_GLOBAL)

# Carrega a biblioteca libReflexao
libCountingPRU = ctypes.CDLL("libCountingPRU.so", mode = ctypes.RTLD_GLOBAL)

# Buffer para contadores
count_buffer = (ctypes.c_uint32 * 6)()


# Procedimento de inicialização da PRU
def Init():
    libCountingPRU.init_start_PRU()


# Enviar um pulso para a rede e verificar descasamento
def Counting(time_base):
    libCountingPRU.Counting(ctypes.c_float(time_base), ctypes.byref(count_buffer))
    answer = []
    for i in range (6):
        answer.append(count_buffer[i])
    return answer



# Encerra a PRU
def Close():
    libCountingPRU.close_PRU()
