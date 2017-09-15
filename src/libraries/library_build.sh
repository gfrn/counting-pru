#!/usr/bin/env sh
gcc -mfloat-abi=hard -Wall -fPIC -O2 -mtune=cortex-a8 -march=armv7-a -I/usr/include -c -o CountingPRU.o CountingPRU.c
ar -rv libCountingPRU.a CountingPRU.o
gcc -shared -Wl,-soname, -o libCountingPRU.so CountingPRU.o
pasm -V3 -b CountLNLS.p
pasm -V3 -b CountBergoz.p



install -m0755 libCountingPRU.a libCountingPRU.so /usr/lib
ldconfig -n /usr/lib/libCountingPRU.*
install -m0755 CountingPRU.h /usr/include

mv CountLNLS.bin /usr/bin
mv CountBergoz.bin /usr/bin

rm CountingPRU.o libCountingPRU.so libCountingPRU.a 
