#!/usr/bin/python
# -*- coding: utf-8 -*-

from pcaspy import Driver, Alarm, Severity, SimpleServer
import sys
import threading
import Reflexao

NBERCOS = 6

PVs = {}

for Berco in range(1,NBERCOS+1):
	PVs["SENSORVAZAMENTO:BERCO" + str(Berco)] = { "type" : "float", "prec" : 2, "unit" : "m" }

PVs["SENSORVAZAMENTO:POSICAO"] = { "type" : "float", "prec" : 2, "unit" : "m" }
PVs["SENSORVAZAMENTO:MODO"] = { "type" : "enum", "enums" : ["MONITORAR", "CALIBRAR"] }


class SV_Driver(Driver):

    def __init__(self):

        Driver.__init__(self)
	Reflexao.Init()

	for Berco in range(1,NBERCOS+1):
	        self.setParamStatus("SENSORVAZAMENTO:BERCO" + str(Berco), Alarm.NO_ALARM, Severity.NO_ALARM)

        for Berco in range(1,NBERCOS+1):
                self.setParam("SENSORVAZAMENTO:BERCO" + str(Berco), Berco + 1.5)



        self.event = threading.Event()
        self.scan = threading.Thread(target = self.scanThread)
        self.scan.setDaemon(True)
        self.scan.start()


    def scanThread(self):
        while (True):
		# Modo calibracao das posicoes
		while self.getParam("SENSORVAZAMENTO:MODO") == 1:
			for Berco in range (1,NBERCOS+1):
				if self.getParam("SENSORVAZAMENTO:BERCO" + str(Berco)) == 0:
					self.setParam("SENSORVAZAMENTO:BERCO" + str(Berco), Reflexao.Pulsar())
					self.updatePVs()
            	
		# Monitoramento: pulsar e armazenar a posicao do vazamento
		self.event.wait(1)
		self.setParam("SENSORVAZAMENTO:POSICAO", Reflexao.Pulsar())
		self.updatePVs()

		# Aguarda proximo monitoramento. Caso modo de calibracao seja selecionado, quebra o delay
		for i in range (0,10):	
	            	self.event.wait(1)
			if self.getParam("SENSORVAZAMENTO:MODO") != 0:
				break
			

    def write(self, reason, value):

	# Nao permite escrita na posicao do vazamento
	if reason == "SENSORVAZAMENTO:POSICAO":
		return (False)

	# Escrita no modo de operacao
        if reason == "SENSORVAZAMENTO:MODO":
		self.setParam(reason, value)
		self.updatePVs()
		return (True)

	# Define berco a ser calibrado somente se em modo CALIBRAR
	if self.getParam("SENSORVAZAMENTO:MODO") == 1:
		self.setParam(reason, value)
		self.updatePVs()
		return (True)

	return (False)

	

if (__name__ == '__main__'):

    CAserver = SimpleServer()
    CAserver.createPV("", PVs)
    driver = SV_Driver()

    while (True):
        CAserver.process(0.1)
