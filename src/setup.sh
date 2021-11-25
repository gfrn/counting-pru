#!/bin/bash

DEBIAN_VERSION=`cut -d . -f 1 <<< cat /etc/debian_version`

echo "== CountingPRU - Installation script =="
echo "Installing Debian $DEBIAN_VERSION version..."

if [ $DEBIAN_VERSION -gt 9 ]; then
    echo "Fetching binaries..."
    make -C v3-0/library

    echo "Installing Python library..."
    cd v3-0/library/Python/
    python3 setup.py install
else
    ./library_build.sh
fi
