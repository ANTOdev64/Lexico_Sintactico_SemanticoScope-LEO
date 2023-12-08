.data
    var_x: .word 0:1
    var_a: .word 0:1
.text
principal:
    li $a0, 3

    sw $a0 0($sp) # Del acumulador a la pila
    add $sp $sp -4 # PUSH

    li $a0, 2

    lw $t1 4($sp) # Del de la pila al temporal
    mult $t1 $a0 # MULTIPLICAR
    mflo $a0
    add $sp $sp 4 # POP 2

    la  $t1, var_a
    sw  $a0, 0($t1)


    # invocacion a una funcion
    sw $fp 0($sp)
    addiu $sp $sp-4

    # generamos codigo para cada parametro
    li $a0, 15

    # metemos el parametro a la pila
    sw $a0 0($sp)
    addiu $sp $sp-4

    jal f1 # invocamos a la funcion


    sw $a0 0($sp) # Del acumulador a la pila
    add $sp $sp -4 # PUSH


    la $t0, var_a
    lw $a0, 0($t0)

    lw $t1 4($sp) # Del de la pila al temporal
    add $a0 $t1 $a0 # SUMAR
    add $sp $sp 4 # POP

    la  $t1, var_x
    sw  $a0, 0($t1)


    # e_1
    la $t0, var_x
    lw $a0, 0($t0)

    # push
    sw $a0, 0($sp)
    add $sp, $sp, -4

    # e_2
    li $a0, 18

    # comparacion
    lw $t1, 4($sp)
    add $sp, $sp, 4
    bgt $a0, $t1, label_false

label_true:

    la $t0, var_x
    lw $a0, 0($t0)

    sw $a0 0($sp) # Del acumulador a la pila
    add $sp $sp -4 # PUSH

    li $a0, 3

    lw $t1 4($sp) # Del de la pila al temporal
    add $a0 $t1 $a0 # SUMAR
    add $sp $sp 4 # POP

    la  $t1, var_x
    sw  $a0, 0($t1)

    b label_end

label_false:

    la $t0, var_a
    lw $a0, 0($t0)

    la  $t1, var_x
    sw  $a0, 0($t1)

label_end:


    # Imprimir x:
    lw $a0, var_x
    li $v0, 1
    syscall

    # Finalizar el main:
    li $v0, 10
    syscall 
f1:
    move $fp $sp

    sw $ra 0($sp)
    addiu $sp $sp -4

    lw $a0, 8($sp)

    sw $a0 0($sp) # Del acumulador a la pila
    add $sp $sp -4 # PUSH

    li $a0, 5

    lw $t1 4($sp) # Del de la pila al temporal
    add $a0 $t1 $a0 # SUMAR
    add $sp $sp 4 # POP


    lw $ra 4($sp)
    addiu $sp $sp 12 # 12 = 4*num_param + 8 
    lw $fp 0($sp)
    jr $ra
