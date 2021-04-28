#!/usr/bin/env sh
/sbin/modprobe uio_pruss


KERNEL_VERSION=`uname -r`;
if [ "${KERNEL_VERSION%.*}" = "3.8" ]; then
    echo "Configuring pins for kernel 3.8.x"
    echo CountingPRU > /sys/devices/bone_capemgr.9/slots
    echo INHIB > /sys/devices/bone_capemgr.9/slots

elif [ "${KERNEL_VERSION%.*}" = "4.14" ]; then
    echo "Configuring pins for kernel 4.14.x"
    # CountingPRU pins
    config-pin P8_15 pruin          # Count1
    config-pin P9_24 pruin          # Count2
    config-pin P8_42 pruin          # Count3
    config-pin P8_41 pruin          # Count4
    config-pin P8_40 pruin          # Count5
    config-pin P8_39 pruin          # Count6
    config-pin P9_30 pruin          # Count7
    config-pin P9_28 pruin          # Count8

    config-pin P8_12 pruout         # Clear1
    config-pin P9_27 pruout         # Clear2
    config-pin P8_45 pruout         # Clear3
    config-pin P8_46 pruout         # Clear4
    config-pin P8_44 pruout         # Clear5
    config-pin P8_43 pruout         # Clear6
    config-pin P9_31 pruout         # Clear7
    config-pin P9_29 pruout         # Clear8

    # Inhibit pins
    config-pin P9_13 out_pd
    config-pin P9_14 out_pd
    config-pin P9_15 out_pd
    config-pin P9_16 out_pd
else
    echo "Version not supported"
fi
