#!/usr/bin/python
# -*- coding: utf-8 -*-


# SI-SiriusBLM-PRU
# Software de Interface - SiriusBLM PRU-based

# Patricia H Nallin
# (Adaptado de Eduardo P Coelho)


# Modulos necessarios
from pcaspy import Driver, Alarm, Severity, SimpleServer
from Queue import PriorityQueue
import traceback
import threading
import time
import serial
import socket
import sys
import CountingPRU


# Configuracao dos BLMs associados a placa
BLMs = ["LNLS1", "LNLS2", "LNLS3", "LNLS4","Bergoz1-Interno", "Bergoz2-Externo"]

# Define as PVs que serao servidas pelo programa
PVs = {}
for module in BLMs:
    if module == "Bergoz1-Interno" or module == "Bergoz2-Externo":
	PVs["UVX:CountingPRU:" + sys.argv[1] + ":" + module] = { "type" : "int", "unit" : "electrons per second"}
    else:
	PVs["UVX:CountingPRU:" + sys.argv[1] + ":" + module] = { "type" : "int", "unit" : "gama per second"}

PVs["UVX:CountingPRU:" + sys.argv[1] + ":TimeBase"] = { "type" : "int", "unit" : "seconds"}



# Inicializacao da biblioteca de contagem
CountingPRU.Init()


# Time String
def time_string():
    return(time.strftime("%d/%m/%Y, %H:%M:%S - ", time.localtime()))

# Driver EPICS para as placas contadoras SiriusBLM-CPLD
class PSDriver(Driver):

    # Construtor da classe
    def __init__(self):

        # Chama o construtor da superclasse
        Driver.__init__(self)

        # Define condicoes iniciais das variáveis EPICS de escrita
        for module in BLMs:
                self.setParam("UVX:CountingPRU:" + sys.argv[1] + ":" + module, 0)
                self.setParamStatus("UVX:CountingPRU:" + sys.argv[1] + ":" + module, Alarm.NO_ALARM, Severity.NO_ALARM)

        self.setParam("UVX:CountingPRU:" + sys.argv[1] + ":TimeBase", 1)
        self.setParamStatus("UVX:CountingPRU:" + sys.argv[1] + ":TimeBase", Alarm.NO_ALARM, Severity.NO_ALARM)

        # Fila de prioridade
        self.queue = PriorityQueue()

        # Objeto do tipo Event para temporizacao das leituras
        self.event = threading.Event()

        # Cria, configura e inicializa as threads
        self.process = threading.Thread(target = self.processThread)
        self.scan = threading.Thread(target = self.scanThread)

        self.process.setDaemon(True)
        self.scan.setDaemon(True)

        self.process.start()
        self.scan.start()


    # Thread que, periodicamente (duas vezes por segundo), enfileira operacao de leitura

    def scanThread(self):
        while (True):
                self.queue.put((1, ["READ_COUNTERS"]))
                self.event.wait(self.getParam("UVX:CountingPRU:" + sys.argv[1] + ":TimeBase"))

    # Thread que processa a fila de operacoes
    def processThread(self):
        # Laco que executa indefinidamente
        while (True):
            # Retira a proxima operacao da fila
            item = self.queue.get(block = True)
            item = item[1]

            # Verifica a operacao a ser realizada

            if (item[0] == "READ_COUNTERS"):

                # Operação de leitura
                # Solicita os valores - BASE DE TEMPO
                Counter = CountingPRU.Counting(self.getParam("UVX:CountingPRU:" + sys.argv[1] + ":TimeBase"))

                # Atualiza os valores das variáveis EPICS e bloco de leitura associados
                for channel in range (len(BLMs)):
                        self.updatePV("UVX:CountingPRU:" + sys.argv[1] + ":" + BLMs[channel], Counter[channel])
                self.updatePVs()


    def updatePV(self, pv_name, new_value):
        update_flag = 0
        if (new_value != self.pvDB[pv_name].value):
            self.setParam(pv_name, new_value)
            update_flag = 1
        if (self.pvDB[pv_name].severity == Severity.INVALID_ALARM):
            self.setParamStatus(pv_name, Alarm.NO_ALARM, Severity.NO_ALARM)
            update_flag = 1
        if (update_flag == 1):
            self.updatePVs()

    # Nao permite escrita em PVs
    def write(self, reason, value):
        if reason[-9:] == ":TimeBase":
            self.setParam(reason, value)
            self.updatePVs()
            return (True)

        else:
            return(False)



# Rotina executada quando o programa e lancado
if (__name__ == '__main__'):

    # Imprime uma mensagem inicial na tela
    sys.stdout.write("SI-SiriusBLM:PRU SiriusBLM - PRU-based\n")
    sys.stdout.write(time_string() + "Programa inicializado.\n")
    sys.stdout.flush()

    # Inicializa o servidor EPICS
    CAserver = SimpleServer()
    CAserver.createPV("", PVs)
    driver = PSDriver()

    # Laco que executa indefinidamente
    while (True):
        CAserver.process(0.1)
