/*
CountingPRU.h
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
#include <unistd.h>
#include <prussdrv.h>
#include <pruss_intc_mapping.h>


#ifdef __cplusplus
extern "C" {
#endif

/* PRU SHARED MEMORY (12kB) - MAPPING
 *
 * prudata[00] = Start/Stop/DataReady flag
 * prudata[01] = Data Ready LNLS
 * prudata[02] = Data Ready Bergoz
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


/* PRU INITIALIZATION
 * --Returns--
 *  0: successfully initialized
 * -1: Error
*/
int init_start_PRU();



/* COUNTING PULSES
 * --Parameters--
 * time_base:	Time base for counting pulses, in seconds
 * Data:		8-position vector for storing counter values
*/
void Counting(float time_base, uint32_t *data);



/* CLOSING PRU
*/
void close_PRU();


#ifdef __cplusplus
}
#endif
