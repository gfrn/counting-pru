// PRU1 - LNLS/Carlos
#define OWN_RAM				0x000
#define OTHER_RAM			0x020
#define SHARED_RAM			0x100

#define START				0xFF
#define STOP				0x00
#define DATAOK				0x55

#define OUT1				r30.t0	// P8.45
#define OUT2				r30.t1	// P8.46
#define OUT3				r30.t3	// P8.44
#define OUT4				r30.t2	// P8.43

#define IN1					r31.t5	// P8.42
#define IN2					r31.t4	// P8.41
#define IN3					r31.t7	// P8.40
#define IN4					r31.t6	// P8.39

#define COUNT1				r16
#define COUNT2				r17
#define	COUNT3				r18
#define COUNT4				r19
#define	COUNT5				r20
#define COUNT6				r21

#define I					r15
#define J					r14


.setcallreg r29.w0				// PC saving register (CALL instructions)
.origin 0						// start of program in PRU memory
.entrypoint BEGINNING			// program entry point (for a debugger)

#include "CountLNLS.hp"
#define AM33XX

// Clear Saidas
BEGINNING:
	SET		SAI1
	SET		SAI2
	SET		SAI3
	SET		SAI4


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
	CLR		OUT1
	SET		OUT1
	CLR		OUT2
	SET		OUT2
	CLR		OUT3
	SET		OUT3
	CLR		OUT4
	SET		OUT4

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




// ----- END! STORE VALUES  --------------------------------------------------------------------
	SBCO	COUNT1, SHRAM_BASE, 4, 4
	SBCO	COUNT2, SHRAM_BASE, 8, 4
	SBCO	COUNT3, SHRAM_BASE, 12, 4
	SBCO	COUNT4, SHRAM_BASE, 16, 4



// ----- Data Ready -----
	MOV		I,DATAOK
	SBCO	I, SHRAM_BASE, 1, 1


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
