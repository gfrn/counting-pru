EESchema Schematic File Version 2
LIBS:power
LIBS:device
LIBS:transistors
LIBS:conn
LIBS:linear
LIBS:regul
LIBS:74xx
LIBS:cmos4000
LIBS:adc-dac
LIBS:memory
LIBS:xilinx
LIBS:microcontrollers
LIBS:dsp
LIBS:microchip
LIBS:analog_switches
LIBS:motorola
LIBS:texas
LIBS:intel
LIBS:audio
LIBS:interface
LIBS:digital-audio
LIBS:philips
LIBS:display
LIBS:cypress
LIBS:siliconi
LIBS:opto
LIBS:atmel
LIBS:contrib
LIBS:valves
LIBS:CountingPRU_v2-2-cache
EELAYER 25 0
EELAYER END
$Descr A4 11693 8268
encoding utf-8
Sheet 3 4
Title "Projeto - Cape Serial 232 e 485 - BeagleBone Black"
Date "2017-06-20"
Rev "v2.2"
Comp "Laboratorio Nacional de Luz Sincrotron - LNLS"
Comment1 "Grupo CON"
Comment2 "Patricia Nallin"
Comment3 ""
Comment4 "Garantia de Reset - Hardware"
$EndDescr
$Comp
L 74HC123 U21
U 1 1 574490D0
P 3450 3525
F 0 "U21" H 3450 3475 50  0000 C CNN
F 1 "74LS123" H 3450 3375 50  0000 C CNN
F 2 "Housings_SOIC:SOIC-16_3.9x9.9mm_Pitch1.27mm" H 3450 3525 50  0001 C CNN
F 3 "" H 3450 3525 50  0000 C CNN
	1    3450 3525
	1    0    0    -1  
$EndComp
$Comp
L 74HC123 U21
U 2 1 57449159
P 5900 3575
F 0 "U21" H 5900 3525 50  0000 C CNN
F 1 "74LS123" H 5900 3425 50  0000 C CNN
F 2 "Housings_SOIC:SOIC-16_3.9x9.9mm_Pitch1.27mm" H 5900 3575 50  0001 C CNN
F 3 "" H 5900 3575 50  0000 C CNN
	2    5900 3575
	1    0    0    -1  
$EndComp
$Comp
L 1G08 U22
U 1 1 57449295
P 7575 3325
F 0 "U22" H 7625 3375 39  0000 C CNN
F 1 "1G08" H 7625 3275 39  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-353_SC-70-5" H 7625 3325 60  0001 C CNN
F 3 "" H 7625 3325 60  0000 C CNN
	1    7575 3325
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR049
U 1 1 57449492
P 7475 3125
F 0 "#PWR049" H 7475 2975 50  0001 C CNN
F 1 "+5V" H 7475 3265 50  0000 C CNN
F 2 "" H 7475 3125 50  0000 C CNN
F 3 "" H 7475 3125 50  0000 C CNN
	1    7475 3125
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR050
U 1 1 574494B3
P 8575 3150
F 0 "#PWR050" H 8575 3000 50  0001 C CNN
F 1 "+5V" H 8575 3290 50  0000 C CNN
F 2 "" H 8575 3150 50  0000 C CNN
F 3 "" H 8575 3150 50  0000 C CNN
	1    8575 3150
	1    0    0    -1  
$EndComp
NoConn ~ 9975 3550
NoConn ~ 9975 3700
NoConn ~ 8575 3550
$Comp
L +5V #PWR051
U 1 1 57449B9C
P 4475 4525
F 0 "#PWR051" H 4475 4375 50  0001 C CNN
F 1 "+5V" H 4475 4665 50  0000 C CNN
F 2 "" H 4475 4525 50  0000 C CNN
F 3 "" H 4475 4525 50  0000 C CNN
	1    4475 4525
	1    0    0    -1  
$EndComp
$Comp
L CP_Small C27
U 1 1 57449C6A
P 3450 2625
F 0 "C27" H 3460 2695 50  0000 L CNN
F 1 "100u" H 3460 2545 50  0000 L CNN
F 2 "Capacitors_Tantalum_SMD:CP_Tantalum_Case-A_EIA-3216-18_Reflow" H 3450 2625 50  0001 C CNN
F 3 "" H 3450 2625 50  0000 C CNN
	1    3450 2625
	0    -1   -1   0   
$EndComp
$Comp
L R_Small R25
U 1 1 57449CF5
P 3050 2625
F 0 "R25" H 3080 2645 50  0000 L CNN
F 1 "910k" H 3080 2585 50  0000 L CNN
F 2 "Resistors_SMD:R_0805" H 3050 2625 50  0001 C CNN
F 3 "" H 3050 2625 50  0000 C CNN
	1    3050 2625
	0    -1   -1   0   
$EndComp
$Comp
L CP_Small C30
U 1 1 57449F00
P 5900 2725
F 0 "C30" H 5910 2795 50  0000 L CNN
F 1 "10u" H 5910 2645 50  0000 L CNN
F 2 "Capacitors_Tantalum_SMD:CP_Tantalum_Case-A_EIA-3216-18_Reflow" H 5900 2725 50  0001 C CNN
F 3 "" H 5900 2725 50  0000 C CNN
	1    5900 2725
	0    -1   -1   0   
$EndComp
$Comp
L R_Small R28
U 1 1 57449F06
P 5500 2725
F 0 "R28" H 5530 2745 50  0000 L CNN
F 1 "220k" H 5530 2685 50  0000 L CNN
F 2 "Resistors_SMD:R_0805" H 5500 2725 50  0001 C CNN
F 3 "" H 5500 2725 50  0000 C CNN
	1    5500 2725
	0    -1   -1   0   
$EndComp
$Comp
L +5V #PWR052
U 1 1 5744A054
P 2775 2625
F 0 "#PWR052" H 2775 2475 50  0001 C CNN
F 1 "+5V" H 2775 2765 50  0000 C CNN
F 2 "" H 2775 2625 50  0000 C CNN
F 3 "" H 2775 2625 50  0000 C CNN
	1    2775 2625
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR053
U 1 1 5744A089
P 5250 2725
F 0 "#PWR053" H 5250 2575 50  0001 C CNN
F 1 "+5V" H 5250 2865 50  0000 C CNN
F 2 "" H 5250 2725 50  0000 C CNN
F 3 "" H 5250 2725 50  0000 C CNN
	1    5250 2725
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR054
U 1 1 5744A1CE
P 5150 3375
F 0 "#PWR054" H 5150 3225 50  0001 C CNN
F 1 "+5V" H 5150 3515 50  0000 C CNN
F 2 "" H 5150 3375 50  0000 C CNN
F 3 "" H 5150 3375 50  0000 C CNN
	1    5150 3375
	0    -1   -1   0   
$EndComp
$Comp
L R_Small R26
U 1 1 5744A352
P 4300 3825
F 0 "R26" H 4330 3845 50  0000 L CNN
F 1 "330r" H 4330 3785 50  0000 L CNN
F 2 "Resistors_SMD:R_0805" H 4300 3825 50  0001 C CNN
F 3 "" H 4300 3825 50  0000 C CNN
	1    4300 3825
	0    1    1    0   
$EndComp
$Comp
L R_Small R29
U 1 1 5744A3CE
P 6750 3875
F 0 "R29" H 6780 3895 50  0000 L CNN
F 1 "330r" H 6780 3835 50  0000 L CNN
F 2 "Resistors_SMD:R_0805" H 6750 3875 50  0001 C CNN
F 3 "" H 6750 3875 50  0000 C CNN
	1    6750 3875
	0    1    1    0   
$EndComp
$Comp
L Led_Small D12
U 1 1 5744A4F0
P 6950 3875
F 0 "D12" H 6900 4000 50  0000 L CNN
F 1 "LED" H 7000 3800 50  0000 L CNN
F 2 "LEDs:LED_0805" V 6950 3875 50  0001 C CNN
F 3 "" V 6950 3875 50  0000 C CNN
	1    6950 3875
	1    0    0    -1  
$EndComp
$Comp
L Led_Small D10
U 1 1 57458C9E
P 4500 3825
F 0 "D10" H 4450 3950 50  0000 L CNN
F 1 "LED" H 4550 3750 50  0000 L CNN
F 2 "LEDs:LED_0805" V 4500 3825 50  0001 C CNN
F 3 "" V 4500 3825 50  0000 C CNN
	1    4500 3825
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR055
U 1 1 57458DAE
P 4600 3825
F 0 "#PWR055" H 4600 3675 50  0001 C CNN
F 1 "+5V" H 4600 3965 50  0000 C CNN
F 2 "" H 4600 3825 50  0000 C CNN
F 3 "" H 4600 3825 50  0000 C CNN
	1    4600 3825
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR056
U 1 1 57458EA3
P 7050 3875
F 0 "#PWR056" H 7050 3725 50  0001 C CNN
F 1 "+5V" H 7050 4015 50  0000 C CNN
F 2 "" H 7050 3875 50  0000 C CNN
F 3 "" H 7050 3875 50  0000 C CNN
	1    7050 3875
	1    0    0    -1  
$EndComp
Text Label 7025 3375 0    60   ~ 0
GPIO
Text Label 6750 3275 0    60   ~ 0
pulsRST
$Comp
L R_Small R27
U 1 1 574DC0DE
P 4475 4625
F 0 "R27" H 4505 4645 50  0000 L CNN
F 1 "10k" H 4505 4585 50  0000 L CNN
F 2 "Resistors_SMD:R_0805" H 4475 4625 50  0001 C CNN
F 3 "" H 4475 4625 50  0000 C CNN
	1    4475 4625
	1    0    0    -1  
$EndComp
$Comp
L C_Small C28
U 1 1 574DC169
P 4475 5000
F 0 "C28" H 4485 5070 50  0000 L CNN
F 1 "100n" H 4485 4920 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805" H 4475 5000 50  0001 C CNN
F 3 "" H 4475 5000 50  0000 C CNN
	1    4475 5000
	1    0    0    -1  
$EndComp
Text Label 3850 4325 2    60   ~ 0
RST_RST
$Comp
L D D9
U 1 1 574DCA21
P 3050 2325
F 0 "D9" H 3050 2425 50  0000 C CNN
F 1 "Schottky" H 3200 2400 50  0000 C CNN
F 2 "Diodes_SMD:D_SOD-323" H 3050 2325 50  0001 C CNN
F 3 "" H 3050 2325 50  0000 C CNN
	1    3050 2325
	1    0    0    -1  
$EndComp
$Comp
L D D11
U 1 1 574DCBF3
P 5525 2475
F 0 "D11" H 5525 2575 50  0000 C CNN
F 1 "Schottky" H 5700 2550 50  0000 C CNN
F 2 "Diodes_SMD:D_SOD-323" H 5525 2475 50  0001 C CNN
F 3 "" H 5525 2475 50  0000 C CNN
	1    5525 2475
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR057
U 1 1 574EF804
P 5400 4700
F 0 "#PWR057" H 5400 4550 50  0001 C CNN
F 1 "+5V" H 5400 4840 50  0000 C CNN
F 2 "" H 5400 4700 50  0000 C CNN
F 3 "" H 5400 4700 50  0000 C CNN
	1    5400 4700
	1    0    0    -1  
$EndComp
$Comp
L C_Small C29
U 1 1 574EFCB5
P 5300 4850
F 0 "C29" H 5310 4920 50  0000 L CNN
F 1 "100n" H 5310 4770 50  0000 L CNN
F 2 "Capacitors_SMD:C_0805" H 5300 4850 50  0001 C CNN
F 3 "" H 5300 4850 50  0000 C CNN
	1    5300 4850
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR058
U 1 1 575200BC
P 7475 3525
F 0 "#PWR058" H 7475 3275 50  0001 C CNN
F 1 "GNDD" H 7475 3375 50  0000 C CNN
F 2 "" H 7475 3525 50  0000 C CNN
F 3 "" H 7475 3525 50  0000 C CNN
	1    7475 3525
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR059
U 1 1 57520104
P 6250 2750
F 0 "#PWR059" H 6250 2500 50  0001 C CNN
F 1 "GNDD" H 6250 2600 50  0000 C CNN
F 2 "" H 6250 2750 50  0000 C CNN
F 3 "" H 6250 2750 50  0000 C CNN
	1    6250 2750
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR060
U 1 1 5752018D
P 3825 2650
F 0 "#PWR060" H 3825 2400 50  0001 C CNN
F 1 "GNDD" H 3825 2500 50  0000 C CNN
F 2 "" H 3825 2650 50  0000 C CNN
F 3 "" H 3825 2650 50  0000 C CNN
	1    3825 2650
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR061
U 1 1 575202D5
P 4475 5150
F 0 "#PWR061" H 4475 4900 50  0001 C CNN
F 1 "GNDD" H 4475 5000 50  0000 C CNN
F 2 "" H 4475 5150 50  0000 C CNN
F 3 "" H 4475 5150 50  0000 C CNN
	1    4475 5150
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR062
U 1 1 57520403
P 8575 3700
F 0 "#PWR062" H 8575 3450 50  0001 C CNN
F 1 "GNDD" H 8575 3550 50  0000 C CNN
F 2 "" H 8575 3700 50  0000 C CNN
F 3 "" H 8575 3700 50  0000 C CNN
	1    8575 3700
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR063
U 1 1 57520444
P 9975 3325
F 0 "#PWR063" H 9975 3075 50  0001 C CNN
F 1 "GNDD" H 9975 3175 50  0000 C CNN
F 2 "" H 9975 3325 50  0000 C CNN
F 3 "" H 9975 3325 50  0000 C CNN
	1    9975 3325
	1    0    0    -1  
$EndComp
Text HLabel 1650 3325 0    60   Input ~ 0
GPIO_RST
Text Label 2000 3325 0    60   ~ 0
GPIO
Text HLabel 10100 3150 2    60   Output ~ 0
HARD_RST
Text Label 4925 4825 2    60   ~ 0
RST_RST
Text Label 6300 4375 2    60   ~ 0
RST_RST
Text Label 7975 3325 0    60   ~ 0
pontoRST
$Comp
L 1G08 U19
U 1 1 57850210
P 2200 3900
F 0 "U19" H 2250 3950 39  0000 C CNN
F 1 "1G08" H 2250 3850 39  0000 C CNN
F 2 "TO_SOT_Packages_SMD:SOT-353_SC-70-5" H 2250 3900 60  0001 C CNN
F 3 "" H 2250 3900 60  0000 C CNN
	1    2200 3900
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR064
U 1 1 57850216
P 2100 3700
F 0 "#PWR064" H 2100 3550 50  0001 C CNN
F 1 "+5V" H 2100 3840 50  0000 C CNN
F 2 "" H 2100 3700 50  0000 C CNN
F 3 "" H 2100 3700 50  0000 C CNN
	1    2100 3700
	1    0    0    -1  
$EndComp
$Comp
L GNDD #PWR065
U 1 1 5785021C
P 2100 4100
F 0 "#PWR065" H 2100 3850 50  0001 C CNN
F 1 "GNDD" H 2100 3950 50  0000 C CNN
F 2 "" H 2100 4100 50  0000 C CNN
F 3 "" H 2100 4100 50  0000 C CNN
	1    2100 4100
	1    0    0    -1  
$EndComp
Text Label 1400 3950 0    60   ~ 0
pontoRST
Text Label 4675 3225 0    60   ~ 0
pulsoWAIT
$Comp
L GNDD #PWR066
U 1 1 5787C688
P 5300 4950
F 0 "#PWR066" H 5300 4700 50  0001 C CNN
F 1 "GNDD" H 5300 4800 50  0000 C CNN
F 2 "" H 5300 4950 50  0000 C CNN
F 3 "" H 5300 4950 50  0000 C CNN
	1    5300 4950
	1    0    0    -1  
$EndComp
$Comp
L GND #PWR067
U 1 1 5787C903
P 4275 5150
F 0 "#PWR067" H 4275 4900 50  0001 C CNN
F 1 "GND" H 4275 5000 50  0000 C CNN
F 2 "" H 4275 5150 50  0000 C CNN
F 3 "" H 4275 5150 50  0000 C CNN
	1    4275 5150
	1    0    0    -1  
$EndComp
$Comp
L TS5A21366 U20
U 1 1 5AA1581D
P 9275 3450
F 0 "U20" H 9750 3875 60  0000 C CNN
F 1 "TS5A21366" H 8975 3875 60  0000 C CNN
F 2 "CONTROLE:VSSOP-8" H 9275 3450 60  0001 C CNN
F 3 "" H 9275 3450 60  0000 C CNN
	1    9275 3450
	1    0    0    -1  
$EndComp
Wire Wire Line
	10100 3150 9975 3150
Wire Wire Line
	6650 3275 7325 3275
Wire Wire Line
	3450 4325 3850 4325
Wire Wire Line
	5900 4375 6300 4375
Wire Wire Line
	6100 2775 6100 2725
Wire Wire Line
	6000 2725 6250 2725
Wire Wire Line
	5600 2725 5800 2725
Wire Wire Line
	5700 2475 5700 2775
Connection ~ 5700 2725
Wire Wire Line
	3550 2625 3825 2625
Wire Wire Line
	3650 2625 3650 2725
Wire Wire Line
	3150 2625 3350 2625
Wire Wire Line
	3250 2325 3250 2725
Connection ~ 3250 2625
Wire Wire Line
	5250 2725 5400 2725
Wire Wire Line
	2775 2625 2950 2625
Wire Wire Line
	4200 3225 5150 3225
Wire Wire Line
	7025 3375 7325 3375
Wire Wire Line
	6250 2725 6250 2750
Connection ~ 6100 2725
Wire Wire Line
	3825 2625 3825 2650
Connection ~ 3650 2625
Wire Wire Line
	4475 4725 4475 4900
Wire Wire Line
	4475 4825 4925 4825
Connection ~ 4475 4825
Wire Wire Line
	3200 2325 3250 2325
Wire Wire Line
	2900 2325 2875 2325
Wire Wire Line
	2875 2325 2875 2625
Connection ~ 2875 2625
Wire Wire Line
	5675 2475 5700 2475
Wire Wire Line
	5375 2475 5350 2475
Wire Wire Line
	5350 2475 5350 2725
Connection ~ 5350 2725
Wire Wire Line
	5300 4750 5300 4700
Wire Wire Line
	1650 3325 2700 3325
Wire Wire Line
	8575 3325 7825 3325
Wire Wire Line
	2700 3175 2650 3175
Wire Wire Line
	2650 3175 2650 3900
Wire Wire Line
	2650 3900 2450 3900
Wire Wire Line
	1950 3850 1850 3850
Wire Wire Line
	1850 3850 1850 3325
Connection ~ 1850 3325
Wire Wire Line
	1950 3950 1400 3950
Wire Wire Line
	4475 5100 4475 5150
Connection ~ 4475 5125
Wire Wire Line
	4275 5150 4275 5125
Wire Wire Line
	4275 5125 4475 5125
Wire Wire Line
	5300 4700 5400 4700
$Comp
L +5V #PWR068
U 1 1 5AA1BB1B
P 5550 3075
F 0 "#PWR068" H 5550 2925 50  0001 C CNN
F 1 "+5V" H 5550 3215 50  0000 C CNN
F 2 "" H 5550 3075 50  0000 C CNN
F 3 "" H 5550 3075 50  0000 C CNN
	1    5550 3075
	1    0    0    -1  
$EndComp
$Comp
L +5V #PWR069
U 1 1 5AA1BBA4
P 3100 3025
F 0 "#PWR069" H 3100 2875 50  0001 C CNN
F 1 "+5V" H 3100 3165 50  0000 C CNN
F 2 "" H 3100 3025 50  0000 C CNN
F 3 "" H 3100 3025 50  0000 C CNN
	1    3100 3025
	1    0    0    -1  
$EndComp
$EndSCHEMATC
