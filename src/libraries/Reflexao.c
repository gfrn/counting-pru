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
#include "Reflexao.h"


#define PRU_NUM             0
#define	PULSAR			0xff
#define PRU_BINARY 		"/usr/bin/Reflexao.bin"



/* PRU SHARED MEMORY (12kB) - MAPPING
 *
 * prudata[0] = pulse verify request
 * prudata[1] = ||
 * prudata[2] = || Response
 * prudata[3] = || Time
 * prudata[4] = ||
 *
 */


volatile uint8_t* prudata;

void close_PRU();
int init_start_PRU();
int pulsar_PRU();


void close_PRU(){
	// ----- Desabilita PRU e fecha mapeamento da shared RAM
	prussdrv_pru_disable(PRU_NUM);
	prussdrv_exit();
}


int init_start_PRU(){

	tpruss_intc_initdata pruss_intc_initdata = PRUSS_INTC_INITDATA;

	// ----- Inicializacao da PRU
	prussdrv_init();

	// ----- Inicializacao da interrupcao PRU
	if (prussdrv_open(PRU_EVTOUT_0))
		return -1; 			// prussdrv_open open failed
	
	prussdrv_pruintc_init(&pruss_intc_initdata);

	// ----- Mapeamento Shared RAM
	prussdrv_map_prumem(PRUSS0_SHARED_DATARAM, (void**)&prudata);
	prudata[0] = 0;

	// ----- Executar codigo na PRU
	prussdrv_exec_program (PRU_NUM, PRU_BINARY);

	return 0;
}


int pulsar_PRU(){

	uint32_t NumberOfInstructions;
	int i = 0,PropagationTime_ns;

	// ----- Sinaliza inicio
	prudata[0] = PULSAR;

	// ----- Aguarda sinal de finalizacao do ciclo
	while(prudata[0]==PULSAR && i<30){
		sleep(0.1);
		i++;	
	}

	// ----- Timeout: Limpa os dados da memoria e reinicializa firmware
	if(prudata[0]){
		prudata[0] = 0;
		prudata[1] = 0;
		prudata[2] = 0;
		prudata[3] = 0;
		prudata[4] = 0;
	    prussdrv_exec_program (PRU_NUM, PRU_BINARY);

	}

	// ----- Calculo do tempo de propagacao
	NumberOfInstructions = (prudata[4] << 24) + (prudata[3] << 16) + (prudata[2] << 8) + (prudata[1]);
	PropagationTime_ns = (int) NumberOfInstructions*5;

	// ----- Compensacao de atrasos intrinsecos ao hardware
	if(PropagationTime_ns != 0)
		PropagationTime_ns -= 35;

	return PropagationTime_ns;
}