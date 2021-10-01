#!/bin/bash

DEBIAN_VERSION=`cut -d . -f 1 <<< cat /etc/debian_version`

echo "== CountingPRU - Installation script =="
echo "Installing Debian $DEBIAN_VERSION version..."

if [ $DEBIAN_VERSION -gt 9 ]; then
    echo "Fetching binaries..."
    mkdir -p bin && cd bin
    wget https://github.com/lnls-sirius/counting-pru/releases/download/v3.0.0/CountingPRU-RProc.tar.gz
    tar -xvzf CountingPRU-RProc.tar.gz
    rm CountingPRU-RProc.tar.gz
    cd ..

    echo "Installing Python library..."
    cd v3-0/library/Python/
    python3 setup.py install
else
    ./library_build.sh
fi
