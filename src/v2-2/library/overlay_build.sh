#!/bin/sh

export SLOTS=/sys/devices/bone_capemgr.9/slots
export PINS=/sys/kernel/debug/pinctrl/44e10800.pinmux/pins

echo "Compilando Device Tree Overlay..."

dtc -O dtb -o CountingPRU-00A0.dtbo -b 0 -@ CountingPRU-00A0.dts
dtc -O dtb -o INHIB-00A0.dtbo -b 0 -@ INHIB-00A0.dts

cp INHIB-00A0.dtbo /lib/firmware
cp CountingPRU-00A0.dtbo /lib/firmware

rm INHIB-00A0.dtbo
rm CountingPRU-00A0.dtbo
