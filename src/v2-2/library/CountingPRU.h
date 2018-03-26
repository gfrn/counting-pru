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

/* INICIALIZACAO DA PRU
 * --Retorno--
 *  0: Ok, bem inicializada
 * -1: Erro
*/
int init_start_PRU();


/* FINALIZACAO DA PRU
 * -----
*/
void close_PRU();


/* CONTAGEM
*/
void Counting(float time, uint32_t *data);





#ifdef __cplusplus
}
#endif
