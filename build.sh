#!/usr/bin/env sh
gcc -mfloat-abi=hard -Wall -O2 -mtune=cortex-a8 -march=armv7-a -I/usr/include -c -o main.o main.c
gcc -static -o main main.o -L/usr/lib -lReflexao -lprussdrv 
rm main.o
