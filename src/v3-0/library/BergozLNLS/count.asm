; PRU0 - CountingPRU

	.define r16, 		COUNT1
	.define r30.t4,		OUT1		; P8_12

	.define r17, 		COUNT2
	.define r30.t5,		OUT2		; P9_27

	.define r18, 		COUNT3
	.define r30.t0,		OUT3		; P9_31

	.define r19, 		COUNT4
	.define r30.t1,		OUT4		; P9_29
	.global asm_count

asm_count:
	ZERO		&COUNT1,4
	ZERO		&COUNT2,4
	ZERO		&COUNT3,4
	ZERO		&COUNT4,4

count1:
	QBBC		count2, r31, 15	; P8_15
	ADD			COUNT1, COUNT1, 1
	CLR			OUT1

count2:
	SET			OUT1
	QBBC		count3, r31, 16
	ADD			COUNT2, COUNT2, 1	; P9_24
	CLR			OUT2

count3:
	SET			OUT2
	QBBC		count4, r31, 2
	ADD			COUNT3, COUNT3, 1	; P9_30
	CLR			OUT3

count4:
	SET			OUT3
	QBBC		ret_loop, r31, 3
	ADD			COUNT4, COUNT4, 1	; P9_28
	CLR			OUT4
ret_loop:
	SET			OUT4
	QBBC   		count1, r31.b3, 6	; If kick bit is set (message received), return

end_count:
	SBBO		&COUNT1, r14, 0, 4
	SBBO		&COUNT2, r14, 4, 4
	SBBO		&COUNT3, r14, 8, 4
	SBBO		&COUNT4, r14, 12, 4	; Copy pulse count to PRU memory
	JMP         r3.w2
