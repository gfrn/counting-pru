/*
CountingPRU.c
v2-2

--------------------------------------------------------------------------------
PRU-based Counters
--------------------------------------------------------------------------------
Interfaces with CountingPRU Hardware (v2-2) in order to count trains of pulses
either from Bergoz Differential BLM or from LNLS Gamma Sensors (4-channel
standard TTL signal)

Brazilian Synchrotron Light Laboratory (LNLS/CNPEM)
Controls Group

Author: Patricia HENRIQUES NALLIN
Date: March/2018
*/

#include <stdio.h>
#include <stdlib.h>
#include <stdint.h>
#include <unistd.h>
#include <prussdrv.h>
#include <pruss_intc_mapping.h>
#include <fcntl.h>
#include <sys/mman.h>
#include <time.h>
#include <signal.h>
#include "CountingPRU.h"

#define PRU_Bergoz_LNLS			0
#define PRU_LNLS				1
#define	START					0xff
#define STOP					0x00
#define DATAOK					0x55
#define PRU_BINARY_Bergoz_LNLS	"/usr/bin/CountBergozLNLS.bin"
#define PRU_BINARY_LNLS			"/usr/bin/CountLNLS.bin"


/* PRU SHARED MEMORY (12kB) - MAPPING
 *
 * prudata[00] = Start/Stop/DataReady flag
 * prudata[01] = Data Ready 1 (Counter Value)
 * prudata[02] = Data Ready 0 (Counter Value)
 * prudata[04..07] = Count 1 LNLS
 * prudata[08..11] = Count 2 LNLS
 * prudata[12..15] = Count 3 LNLS
 * prudata[16..19] = Count 4 LNLS
 * prudata[20..23] = Count 5 LNLS
 * prudata[24..27] = Count 6 LNLS
 * prudata[28..31] = Count 1 Bergoz
 * prudata[35..35] = Count 2 Bergoz
 *
 */

volatile uint8_t* prudata;


int init_start_PRU(){
	int i;

	tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;

	// ----- PRU first initialization
	prussdrv_init();

	// ----- PRU interruption initialization
	if (prussdrv_open(PRU_EVTOUT_1)){
		printf("prussdrv_open open failed\n");
		return -1;
	}
	prussdrv_pruintc_init(&pruss_intc_initdata);

	// ----- Shared RAM mapping and initializing bytes as 0x00
	prussdrv_map_prumem(PRUSS0_SHARED_DATARAM, (void**)&prudata);

	for(i=0; i<36; i++)
		prudata[i] = 0;

	// ----- Run binaries in parallel in both PRUs
	prussdrv_exec_program(PRU_LNLS, PRU_BINARY_LNLS);
	prussdrv_exec_program(PRU_Bergoz_LNLS, PRU_BINARY_Bergoz_LNLS);

	return 0;
}


void Counting(float time_base, uint32_t *data){

	int i;

	// ----- Says it is time to start counting
	prudata[0] = START;

	// ----- Delay: pre-defined Time Base
	sleep(time_base);

	// ----- Says it is time to stop counting
	prudata[0] = STOP;


	// ----- Wait until values of both counters are available in shared RAM
	while(prudata[1] != 0x55){
	}
	while(prudata[2] != 0x55){
	}


	// ----- Get counting values
	for(i=1; i<=8; i++)
		data[i-1] = (prudata[(i*4)+3]<<24) + (prudata[(i*4)+2]<<16) + (prudata[(i*4)+1]<<8) + (prudata[(i*4)]);


	// ----- Counting values successfully copied
	prudata[1] = 0;
	prudata[2] = 0;


	return;
}


void close_PRU(){
	// ----- Disables PRU and closes shared RAM memory mapping
	prussdrv_pru_disable(PRU_LNLS);
	prussdrv_pru_disable(PRU_Bergoz_LNLS);
	prussdrv_exit();
}
