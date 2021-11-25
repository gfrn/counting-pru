PRU_SWPKG = /usr/lib/ti/pru-software-support-package

CC = clpru
LD = lnkpru
CFLAGS = --include_path=$(PRU_SWPKG)/include \
        --include_path=$(PRU_SWPKG)/include/am335x \
        -v3 -O4 --opt_for_speed=5 --endian=little \
        --define=am3359 --define=pru1 --hardware_mac=on --verbose
LDFLAGS = AM335x_PRU.cmd

SRCS = $(wildcard *.c)
PROGS = $(patsubst %.c,%,$(SRCS))

ASM_SRCS = $(wildcard *.asm)
ASM_PROGS = $(patsubst %.asm,%,$(ASM_SRCS))

OUT = ../../../../bin

all: directories $(OUT)/pru0.out $(OUT)/pru1.out

directories: $(OUT)

$(OUT):
	mkdir -p ../../../../bin

$(OUT)/pru1.out:
	$(MAKE) -C LNLS

$(OUT)/pru0.out:
	$(MAKE) -C BergozNLS

clean:
	rm -rf $(OUT)/bin $(ASM_PROGS) $(PROGS)
