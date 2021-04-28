#!/usr/bin/python2
# -*- coding: utf-8 -*-


# SI-SiriusBLM-PRU - Baseboard v2-2
# Software de Interface - SiriusBLM PRU-based

# Patricia H Nallin
# (Adaptado de Eduardo P Coelho)


# Modulos necessarios
from pcaspy import Driver, Alarm, Severity, SimpleServer
from Queue import PriorityQueue
import Adafruit_BBIO.GPIO as GPIO
import traceback
import threading
import time
import serial
import socket
import sys
import CountingPRU



# Configuracao dos BLMs associados a placa
BLMs = ["LNLS1", "LNLS2", "LNLS3", "LNLS4", "LNLS5", "LNLS6", "Bergoz1", "Bergoz2"]

# Pinos Inhibit
InhA1 = "P9_14"
InhB1 = "P9_16"
InhA2 = "P9_13"
InhB2 = "P9_15"

GPIO.setup(InhA1, GPIO.OUT)
GPIO.output(InhA1, GPIO.LOW)
GPIO.setup(InhB1, GPIO.OUT)
GPIO.output(InhB1, GPIO.LOW)

GPIO.setup(InhA2, GPIO.OUT)
GPIO.output(InhA2, GPIO.LOW)
GPIO.setup(InhB2, GPIO.OUT)
GPIO.output(InhB2, GPIO.LOW)


# Define as PVs que serao servidas pelo programa
PVs = {}
for module in BLMs:
    if module == "Bergoz1" or module == "Bergoz2":
	PVs["UVX:CountingPRU:" + sys.argv[1] + ":" + module] = { "type" : "int", "unit" : "electrons per second"}
	PVs["UVX:CountingPRU:" + sys.argv[1] + ":" + module + "-InhA"] = { "type" : "enum", "enums" : ["off", "on"]}
        PVs["UVX:CountingPRU:" + sys.argv[1] + ":" + module + "-InhB"] = { "type" : "enum", "enums" : ["off", "on"]}
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
		if module == "Bergoz1" or module == "Bergoz2":
			self.setParam("UVX:CountingPRU:" + sys.argv[1] + ":" + module + "-InhA", 0)
			self.setParam("UVX:CountingPRU:" + sys.argv[1] + ":" + module + "-InhB", 0)
			self.setParamStatus("UVX:CountingPRU:" + sys.argv[1] + ":" + module + "-InhA", Alarm.NO_ALARM, Severity.NO_ALARM)
			self.setParamStatus("UVX:CountingPRU:" + sys.argv[1] + ":" + module + "-InhB", Alarm.NO_ALARM, Severity.NO_ALARM)


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
                        self.setParam("UVX:CountingPRU:" + sys.argv[1] + ":" + BLMs[channel], Counter[channel])
                self.updatePVs()



    # Nao permite escrita em PVs
    def write(self, reason, value):

        if reason[-9:] == ":TimeBase":
            self.setParam(reason, value)
            self.updatePVs()
            return (True)

	# Modo Calibracao
	elif reason[-6:-1] == "1-Inh":
		if reason[-1:] == "A":
			if value:
				GPIO.output(InhA1, GPIO.HIGH)
			else:
				GPIO.output(InhA1, GPIO.LOW)

		elif reason[-1:] == "B": 
			if value:
                                GPIO.output(InhB1, GPIO.HIGH)
                        else:
                                GPIO.output(InhB1, GPIO.LOW)

		self.setParam(reason, value)
            	self.updatePVs()
            	return (True)

	elif reason[-6:-1] == "2-Inh":	
		if reason[-1:] == "A":
                        if value:
                                GPIO.output(InhA2, GPIO.HIGH)
                        else:
                                GPIO.output(InhA2, GPIO.LOW)

                elif reason[-1:] == "B":
                        if value:
                                GPIO.output(InhB2, GPIO.HIGH)
                        else:
                                GPIO.output(InhB2, GPIO.LOW)

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
