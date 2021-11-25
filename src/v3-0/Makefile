PRU_SWPKG = /usr/lib/ti/pru-software-support-package

OUT = ../../../../bin

all: directories $(OUT)/pru0.out $(OUT)/pru1.out

directories: $(OUT)

$(OUT):
	mkdir -p $(OUT)

$(OUT)/pru1.out:
	$(MAKE) -C LNLS

$(OUT)/pru0.out:
	$(MAKE) -C BergozLNLS

clean:
	$(MAKE) -C LNLS clean
	$(MAKE) -C BergozLNLS clean
