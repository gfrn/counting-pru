// PRU0 - BERGOZ and LNLS
#define OWN_RAM              		0x000
#define OTHER_RAM           		0x020
#define SHARED_RAM          	 	0x100

#define START				0xFF
#define STOP				0x00
#define DATAOK				0x55

#define SAI4				r30.t1		// P9.29 | LNLS 6
#define SAI3				r30.t0		// P9.31 | LNLS 5
#define SAI2				r30.t5		// P9.27 | Bergoz 2
#define SAI1				r30.t14		// P8.12 | Bergoz 1

#define ENT4				r31.t3		// P9.28 | LNLS 6
#define ENT3				r31.t2		// P9.30 | LNLS 5
#define ENT2				r31.t16		// P9.24 | Bergoz 2
#define ENT1				r31.t15		// P8.15 | Bergoz 1

#define COUNT1				r16
#define COUNT2				r17
#define COUNT3				r18
#define COUNT4				r19

#define I				r15
#define J				r14


.setcallreg r29.w0					// PC saving register (CALL instructions)				
.origin 0						// start of program in PRU memory
.entrypoint COMECA					// program entry point (for a debugger)

#include "CountBergozLNLS.hp"
#define AM33XX

// Clear Saidas
COMECA:
	SET	SAI1
	SET	SAI2
	SET	SAI3
	SET	SAI4


// Clear Contadores e Registradores
 	ZERO	&COUNT1,4
	ZERO	&COUNT2,4
	ZERO	&COUNT3,4
	ZERO	&COUNT4,4
	ZERO	&I, 4 
	ZERO	&J, 4 

//  Shared Memory Config
	SHRAM_CONFIG
					

// ----- WAIT START --------------------------------------------------------------------
INICIO: 
        LBCO    I, SHRAM_BASE, 0, 1         		// Load Status Status
	QBNE	INICIO, I, START			// Wait until == 0xFF = Start


// ----- COUNT! --------------------------------------------------------------------
	CLR	SAI1
	SET	SAI1
	CLR	SAI2
	SET	SAI2
	CLR	SAI3
	SET	SAI3
	CLR	SAI4
	SET	SAI4

// ----- 1 -----
CONTA1:
	QBBC	FIM1, ENT1		// Jump, se nao ha pulso
	ADD	COUNT1, COUNT1, 1	// ||
	CLR	SAI1			// || Conta +1 e zera pulso
FIM1:	SET	SAI1			// ||


// ----- 2 -----
CONTA2:
	QBBC	FIM2, ENT2		// Jump, se nao ha pulso
	ADD	COUNT2, COUNT2, 1	// ||
	CLR	SAI2			// || Conta +1 e zera pulso
FIM2:	SET	SAI2			// ||


// ----- 3 -----
CONTA3:
	QBBC	FIM3, ENT3		// Jump, se nao ha pulso
	ADD	COUNT3, COUNT3, 1	// ||
	CLR	SAI3			// || Conta +1 e zera pulso
FIM3:	SET	SAI3			// ||


// ----- 4 -----
CONTA4:
	QBBC	FIM4, ENT4		// Jump, se nao ha pulso
	ADD	COUNT4, COUNT4, 1	// ||
	CLR	SAI4			// || Conta +1 e zera pulso
FIM4:	SET	SAI4			// ||	

// ----- VERIFY END --------------------------------------------------------------------
V_END:
        LBCO    I, SHRAM_BASE, 0, 1         		// Load Status
	QBNE	CONTA1, I, STOP				// Wait until == 0x00 = Stop



// ----- END! STORE VALUES  --------------------------------------------------------------------
	SBCO	COUNT1, SHRAM_BASE, 28, 4 // Bergoz 1
	SBCO	COUNT2, SHRAM_BASE, 32, 4 // Bergoz 2
	SBCO	COUNT3, SHRAM_BASE, 20, 4 // LNLS 5
	SBCO	COUNT4, SHRAM_BASE, 24, 4 // LNLS 6



// ----- Data Ready -----
	MOV	I,DATAOK
	SBCO	I, SHRAM_BASE, 2, 1
	


// Clear Contadores e Registradores
 	ZERO	&COUNT1,4
	ZERO	&COUNT2,4
	ZERO	&COUNT3,4
	ZERO	&COUNT4,4
	ZERO	&I, 4 
	ZERO	&J, 4 

	JMP	INICIO

// Never reached	
END:
	HALT
	
	

	
	
