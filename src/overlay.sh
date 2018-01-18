#!/usr/bin/env sh
/sbin/modprobe uio_pruss
echo CountingPRU > /sys/devices/bone_capemgr.9/slots
echo INHIB > /sys/devices/bone_capemgr.9/slots

cat /sys/devices/bone_capemgr.9/slots

