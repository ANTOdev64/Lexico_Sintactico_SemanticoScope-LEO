.data
    var_x: .word 0:1
    var_yi: .word 0:1
    var_h: .word 0:1
.text
main:
    li $a0, 5

    la  $t1, var_h
    sw  $a0, 0($t1)

    li $a0, 5

    la  $t1, var_x
    sw  $a0, 0($t1)


    la $t0, var_x
    lw $a0, 0($t0)

    sw $a0 0($sp) # Del acumulador a la pila
    add $sp $sp -4 # PUSH

    li $a0, 10

    lw $t1 4($sp) # Del de la pila al temporal
    add $a0 $t1 $a0 # SUMAR
    add $sp $sp 4 # POP

    sw $a0 0($sp) # Del acumulador a la pila
    add $sp $sp -4 # PUSH
 

    la $t0, var_h
    lw $a0, 0($t0)

    lw $t1 4($sp) # Del de la pila al temporal
    add $a0 $t1 $a0 # SUMAR
    add $sp $sp 4 # POP

    la  $t1, var_yi
    sw  $a0, 0($t1)


    # Imprimir yi:
    lw $a0, var_yi
    li $v0, 1
    syscall

    # Finalizar el main:
    li $v0, 10  
    syscall 
