##	lab1_integer_double.s 
##	This program read in an integer and double it

#########################################################
#					DATA SEGMENT						#
#	This is where all strings, constants are declared	#
#########################################################

		.data		# the data segment
msg: 		.asciiz "LTNga\n"
prompt:		.asciiz	"Enter an integer: "
result: 	.asciiz "The result is: "

#########################################################
#					TEXT SEGMENT						#
#	This is where all the instructions reside			#
#########################################################

		.text		# the code segment
		.globl main
main:
	# print out your name
	la $a0, msg
	li $v0, 4
	syscall
	
	# print out the prompt
	la $a0, prompt		
	li $v0, 4		
	syscall		
	
	# read in an integer  stored v0
	li $v0, 5			
	syscall
	move $t0, $v0 #copy the value v0 to t0
	
	# double the input value
	sll $t0, $t0, 1  # result stored in t0
	
	# print out the result message
	la $a0, result		
	li $v0, 4		
	syscall	
	
	# print out the doubled integer
	move $a0, $t0  #copy t0 to a0  li $a0, ...
	li $v0, 1		
	syscall	
	
	jr $ra			# return to caller (__start)
