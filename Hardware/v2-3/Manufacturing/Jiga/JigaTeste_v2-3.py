#bibliotecas
import CountingPRU
import Adafruit_BBIO.GPIO as GPIO
import time


#setup das portas a serem usadas: led, bergoz1A, bergoz1B, bergoz2A, bergoz2B
GPIO.setup("P8_8",GPIO.OUT)
GPIO.setup("P9_14",GPIO.OUT)
GPIO.setup("P9_16",GPIO.OUT)
GPIO.setup("P9_13",GPIO.OUT)
GPIO.setup("P9_15",GPIO.OUT)

GPIO.output("P8_8",GPIO.LOW)


#inicializacao programa
CountingPRU.Init()

#lista de contagem
c=CountingPRU.Counting(1)
print ("\n")
print ("\n")
print (c[:8])

#seleciona canais 1,2,3 para analisar
d=c[:3] 							# lista valores dos 3 1os canais
teste = 1 							# variavel que indica qual canal esta sendo testado
testesensoresOK= 0 						# variavel que indica sucesso de testes

#seleciona canais 4,5,6 para analisar
D=c[3:6]			        			# lista valores dos canais 4,5,6


#verificacao dos canais 1,2,3
print ("Sensor1:{}".format(d))

while teste<4 :
	for index, value in enumerate(d):
		if 1000<value<1800:
			print ("Sensor1 canal %f ok ") %index
			testesensoresOK=testesensoresOK+1

		else:
			print ("Sensor1 canal %f nao funcionando") %index

		teste = teste+1


#verificacao dos canais 4,5,6
print ("\n")
print ("Sensor2:{}".format(D))
while 3<teste<7:
	for index, value in enumerate(D):
		if 3600>value>2800:
			print ("Sensor2 canal %f ok ") %index
			testesensoresOK=testesensoresOK+1

		else:
			print ("Sensor2 canal %f nao funcionando") %index

		teste = teste+1

if testesensoresOK>5:
	print ("\n")
	print ("TESTE DOS SENSORES DE GAMA REALIZADOS COM SUCESSO")
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(0.15)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(0.25)
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(0.15)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(1)

else:
	print ("\n")
	print ("FALHA NOS TESTES DOS SENSORES DE GAMA")
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(2)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(1)



















#VERIFICACAO BERGOZ

#verificacao do bergoz1A:
#configuracao pinos bergoz para B1A
GPIO.output("P8_8",GPIO.LOW)
GPIO.output("P9_14",GPIO.HIGH)
time.sleep(0.1)
c=CountingPRU.Counting(1)
CountB1 = c[6]							#variavel de contagem para bergoz 1
canal1=0
print ("\n")
print (CountB1)
if 11500>CountB1>8000:
	print ("Bergoz 1A ok")
	canal1=canal1+1
else:
	print ("Falha Bergoz 1A")


GPIO.output("P9_14",GPIO.LOW)



#verificacao do bergoz 1B:
#configuracao
GPIO.output("P9_16",GPIO.HIGH)
time.sleep(0.1)
c=CountingPRU.Counting(1)
CountB1 = c[6]
print (CountB1)

if 11500>CountB1>8000:
	print ("Bergoz 1B ok")
	canal1=canal1+1
else:
	print ("Falha Bergoz 1B")


GPIO.output("P9_16",GPIO.LOW)
time.sleep(1)










# verificacao bergoz 2:
#verificacao do bergoz2A:
GPIO.output("P9_13",GPIO.HIGH)
time.sleep(0.1)
c=CountingPRU.Counting(1)
CountB2 = c[7]							#variavel de contagem para bergoz 1
canal2=0
print ("\n")
print (CountB2)

if 11500>CountB2>8000:
	print ("Bergoz 2A ok")
	canal2=canal2+1
else:
	print ("Falha Bergoz 2A")


GPIO.output("P9_13",GPIO.LOW)


#verificacao do bergoz 2B:
GPIO.output("P9_15",GPIO.HIGH)
time.sleep(0.1)
c=CountingPRU.Counting(1)
CountB2 = c[7]
print CountB2

if 11500>CountB2>8000:
	print ("Bergoz 2B ok")
	canal2=canal2+1
else:
	print ("Falha Bergoz 2B")






#caso testes de B1 e B2 sejam bem sucedidos, led pisca 3 vezes:
if canal2==2 and canal1==2:
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(0.15)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(0.25)
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(0.15)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(0.25)
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(0.15)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(0.5)

#caso testes de B1 e/ou B2 sejam mal sucedidos, led pisca 2 vezes com 2s cada pulso:
else:
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(2)
	GPIO.output("P8_8",GPIO.LOW)
	time.sleep(0.2)
	GPIO.output("P8_8",GPIO.HIGH)
	time.sleep(2)

GPIO.output("P9_15",GPIO.LOW)
GPIO.output("P8_8",GPIO.LOW)
time.sleep(2)






#RESULTADO FINAL
#caso ambos os testes forem bem sucedidos:
if canal2==2 and canal1==2 and testesensoresOK==3 :
	GPIO.output("P8_8",GPIO.HIGH)
else:
	GPIO.output("P8_8",GPIO.LOW)


while True:
	continue


