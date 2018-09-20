#!/usr/bin/env sh
cd library

echo "********** COUNTING PRU **********"

KERNEL_VERSION=`uname -r`;
if [ "${KERNEL_VERSION%.*}" = "3.8" ]; then
    echo "."
    echo ".."
    echo "..."
    echo "Building Device Tree Overlay..."
    ./overlay_build.sh
    echo "OK"
fi


echo "."
echo ".."
echo "..."
echo "Building and installing C library..."
gcc -mfloat-abi=hard -Wall -fPIC -O2 -mtune=cortex-a8 -march=armv7-a -I/usr/include -c -o CountingPRU.o CountingPRU.c
ar -rv libCountingPRU.a CountingPRU.o
gcc -shared -Wl,-soname, -o libCountingPRU.so CountingPRU.o
pasm -V3 -b CountLNLS.p
pasm -V3 -b CountBergozLNLS.p



install -m0755 libCountingPRU.a libCountingPRU.so /usr/lib
ldconfig -n /usr/lib/libCountingPRU.*
install -m0755 CountingPRU.h /usr/include

mv CountLNLS.bin /usr/bin
mv CountBergozLNLS.bin /usr/bin

rm CountingPRU.o libCountingPRU.so libCountingPRU.a
echo "OK"


echo "."
echo ".."
echo "..."
echo "Building and installing Python library..."
python2 setup.py install
python-sirius setup.py install
echo "OK"

echo "."
echo ".."
echo "..."
echo "Done!"

cd ..
