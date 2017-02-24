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

# Importa o módulo ctypes
import ctypes

# Carrega as bibliotecas dinâmicas das quais a biblioteca libPRUserial485 depende (bibliotecas da
# PRU)
ctypes.CDLL("libprussdrv.so", mode = ctypes.RTLD_GLOBAL)
ctypes.CDLL("libprussdrvd.so", mode = ctypes.RTLD_GLOBAL)

# Carrega a biblioteca libReflexao
libReflexao = ctypes.CDLL("libReflexao.so", mode = ctypes.RTLD_GLOBAL)


# Procedimento de inicialização da PRU
def Init():
    libReflexao.init_start_PRU()


# Enviar um pulso para a rede e verificar descasamento
def Pulsar():
    return(libReflexao.pulsar_PRU())


# Encerra a PRU
def Close():
    libReflexao.close_PRU()
