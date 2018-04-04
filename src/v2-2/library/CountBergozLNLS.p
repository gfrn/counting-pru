// PRU0 - BERGOZ and LNLS
#define OWN_RAM				0x000
#define OTHER_RAM			0x020
#define SHARED_RAM			0x100

#define START				0xFF
#define STOP				0x00
#define DATAOK				0x55

#define OUT4				r30.t1	// P9.29 | LNLS 6
#define OUT3				r30.t0	// P9.31 | LNLS 5
#define OUT2				r30.t5	// P9.27 | Bergoz 2
#define OUT1				r30.t14	// P8.12 | Bergoz 1

#define IN4					r31.t3	// P9.28 | LNLS 6
#define IN3					r31.t2	// P9.30 | LNLS 5
#define IN2					r31.t16	// P9.24 | Bergoz 2
#define IN1					r31.t15	// P8.15 | Bergoz 1

#define COUNT1				r16
#define COUNT2				r17
#define COUNT3				r18
#define COUNT4				r19

#define I					r15
#define J				   	r14


.setcallreg r29.w0			 // PC saving register (CALL instructions)
.origin 0					 // start of program in PRU memory
.entrypoint BEGINNING		 // program entry point (for a debugger)

#include "CountBergozLNLS.hp"
#define AM33XX

// Clear Outputs
BEGINNING:
	SET	OUT1
	SET	OUT2
	SET	OUT3
	SET	OUT4


// Clear Counters and Registers
 	ZERO	&COUNT1,4
	ZERO	&COUNT2,4
	ZERO	&COUNT3,4
	ZERO	&COUNT4,4
	ZERO	&I, 4
	ZERO	&J, 4

//  Shared Memory Config
	SHRAM_CONFIG


// ----- WAIT START --------------------------------------------------------------------
START_LOOP:
	LBCO	I, SHRAM_BASE, 0, 1			// Load Status Status
	QBNE	START_LOOP, I, START		// Wait until == 0xFF = Start


// ----- START COUNTING! ---------------------------------------------------------------
	CLR	OUT1
	SET	OUT1
	CLR	OUT2
	SET	OUT2
	CLR	OUT3
	SET	OUT3
	CLR	OUT4
	SET	OUT4

// ----- 1 -----
C1:
	QBBC	END1, IN1			   	// Jump, se nao ha pulso
	ADD		COUNT1, COUNT1, 1	   	// ||
	CLR		OUT1					// || Conta +1 e zera pulso
END1:
	SET		OUT1


// ----- 2 -----
C2:
	QBBC	END2, IN2				// Jump, se nao ha pulso
	ADD		COUNT2, COUNT2, 1		// ||
	CLR		OUT2					// || Conta +1 e zera pulso
END2:
	SET		OUT2


// ----- 3 -----
C3:
	QBBC	END3, IN3				// Jump, se nao ha pulso
	ADD		COUNT3, COUNT3, 1		// ||
	CLR		OUT3					// || Conta +1 e zera pulso
END3:
	SET		OUT3


// ----- 4 -----
C4:
	QBBC	END4, IN4				// Jump, se nao ha pulso
	ADD		COUNT4, COUNT4, 1		// ||
	CLR		OUT4					// || Conta +1 e zera pulso
END4:
	SET		OUT4

// ----- VERIFY END ------------------------------------------------------------
V_END:
	LBCO	I, SHRAM_BASE, 0, 1		// Load Status
	QBNE	C1, I, STOP				// Wait until == 0x00 = Stop



// ----- END! STORE VALUES  ----------------------------------------------------
	SBCO	COUNT1, SHRAM_BASE, 28, 4 // Bergoz 1
	SBCO	COUNT2, SHRAM_BASE, 32, 4 // Bergoz 2
	SBCO	COUNT3, SHRAM_BASE, 20, 4 // LNLS 5
	SBCO	COUNT4, SHRAM_BASE, 24, 4 // LNLS 6



// ----- Data Ready -----
	MOV		I,DATAOK
	SBCO	I, SHRAM_BASE, 2, 1



// Clear Counters and Registers
 	ZERO	&COUNT1,4
	ZERO	&COUNT2,4
	ZERO	&COUNT3,4
	ZERO	&COUNT4,4
	ZERO	&I, 4
	ZERO	&J, 4

	JMP		START_LOOP

// Never reached
END:
	HALT
