from sintactico import nodoPadre
from semanticoScope import symbol_table

print("\nIniciando geeración de código en ensamblador MIPS\n")

class TypeDataError(Exception):
    pass

def generar_assembly(instruccion):
    global codigo_assembly
    codigo_assembly.append(instruccion)

codigo_assembly = []

def agrear_pila(instruccion):
    global pila_expresion
    pila_expresion.append(instruccion)

pila_expresion = []

codigo_assembly.append(".data")

for symbol in symbol_table.symbols:
    if symbol['is_function'] == False and symbol['data_type'] == "entero" and symbol['scope'] == "principal":
        generar_assembly(f"    var_{symbol['name']}: .word 0:1")


codigo_assembly.append(".text")

acum_pila = True

tipo_prev = None

op_actual = []
signo_actual = ""

def tatarabuelo(nodo, tata):
    if nodo.Symbol_lexer == tata:
        return True
    
    if nodo.padre is None:
        return False

    return tatarabuelo(nodo.padre, tata)

def recorrer_arbol(nodo):
    global tipo_prev
    global tipo_actual
    global scope_actual
    global tipo_scope_actual


    global acum_pila
    global variable_actual
    global op_actual
    global signo_actual

    if nodo.Symbol_lexer == "FUNCTION":
        tipo_scope_actual = nodo.children[0].children[0].children[0].value
        scope_actual = nodo.children[2].value
        if nodo.children[2].value != "principal":
            generar_assembly(f"    move $fp $sp")
            
            generar_assembly(f"\n    sw $ra 0($sp)")
            generar_assembly(f"    addiu $sp $sp -4")

            generar_assembly(f"\n    lw $a0, 8($sp)")


    elif nodo.Symbol_lexer == "Crear_variables":
        variable_actual = nodo.children[1].value

    elif nodo.Symbol_lexer == "Asig_varibles":
        variable_actual = nodo.children[0].value

    # LUEGO DEL IGUAL =

    elif nodo.Symbol_lexer == "E":
        if nodo.children[0].Symbol_lexer == "CADENA":
            nombre_variable = nodo.children[0].value
            tipo_actual = nombre_variable

    elif nodo.Symbol_lexer == "FH":
        if nodo.children[0].Symbol_lexer == "NUMERO":
            nombre_variable = nodo.children[0].value
            tipo_actual = nombre_variable
            generar_assembly(f"    li $a0, {nodo.children[0].value}")

        elif nodo.children[0].Symbol_lexer == "DECIMAL":
            nombre_variable = nodo.children[0].value
            tipo_actual = nombre_variable

        elif nodo.children[0].Symbol_lexer == "ID":
            nombre_variable = nodo.children[0].value
            info_variable = symbol_table.lookup(nombre_variable, scope_actual)
            if info_variable and 'name' in info_variable:
                tipo_actual = info_variable['name']
                if info_variable['scope'] == "principal":
                    generar_assembly(f"\n    la $t0, var_{info_variable['name']}")
                    generar_assembly(f"    lw $a0, 0($t0)")
            else:
                info_variable = symbol_table.lookup(nombre_variable, "global")
                if info_variable and 'data_type' in info_variable:
                    tipo_actual = info_variable['data_type']

    elif nodo.Symbol_lexer in ["SUMA", "RESTA", "MULTIPLICAR", "DIVIDIR"]:
        tipo_prev = tipo_actual

        op_actual = [] 

        if nodo.Symbol_lexer == "SUMA":
            op_actual.append(f"    add $a0 $t1 $a0 # SUMAR")
        if nodo.Symbol_lexer == "RESTA":
            op_actual.append(f"    sub $a0 $t1 $a0 # RESTAR")
        if nodo.Symbol_lexer == "MULTIPLICAR":
            op_actual.append(f"    mult $t1 $a0 # MULTIPLICAR")
            op_actual.append(f"    mflo $a0")
        if nodo.Symbol_lexer == "DIVIDIR":
            op_actual.append(f"    div $t1, $a0 # DIVIDIR")
            op_actual.append(f"    mflo $a0")

    if nodo.Symbol_lexer == "E'":
        if nodo.children:
            if acum_pila: 
                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n")
                acum_pila = False
            else: 
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n ")

                acum_pila = False
        else:
            if nodo.padre.Symbol_lexer != "E":
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                acum_pila = True

    if nodo.Symbol_lexer == "T'":
        if nodo.children:
            if acum_pila: 
                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n")
                acum_pila = False
            else: 
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                generar_assembly(f"\n    sw $a0 0($sp) # Del acumulador a la pila")
                generar_assembly(f"    add $sp $sp -4 # PUSH\n ")

                acum_pila = False
        else:
            if nodo.padre.Symbol_lexer != "T":
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP 2")
                acum_pila = True
        
    if nodo.Symbol_lexer == "E'":
        if not nodo.children:
            tipo_prev = tipo_scope_actual
            generar_assembly(f"")

            if not tatarabuelo(nodo, "RTN"):
                generar_assembly(f"    la  $t1, var_{variable_actual}")
                generar_assembly(f"    sw  $a0, 0($t1)\n")

    elif nodo.Symbol_lexer == "ID":
        if nodo.padre.Symbol_lexer == "TX":
            generar_assembly(f"\n    # Imprimir {nodo.value}:")
            generar_assembly(f"    lw $a0, var_{nodo.value}")
            generar_assembly(f"    li $v0, 1")
            generar_assembly(f"    syscall")

    # Llamado de funciones

    if nodo.Symbol_lexer == "FN":
        if nodo.children and nodo.padre.children[0].Symbol_lexer == "ID":
            generar_assembly(f"\n    # invocacion a una funcion")
            generar_assembly(f"    sw $fp 0($sp)")
            generar_assembly(f"    addiu $sp $sp-4")

    if nodo.Symbol_lexer == "F'":
        if tatarabuelo(nodo, "FN"):
            generar_assembly(f"\n    # generamos codigo para cada parametro")
            generar_assembly(f"    li $a0, {nodo.children[0].value}")

            generar_assembly(f"\n    # metemos el parametro a la pila")
            generar_assembly(f"    sw $a0 0($sp)")
            generar_assembly(f"    addiu $sp $sp-4")

    if nodo.Symbol_lexer == "PARENTESIS_CERRADO":
        if nodo.padre.Symbol_lexer == "FN":
            if nodo.padre.padre.children[0].Symbol_lexer == "ID":
                generar_assembly(f"\n    jal {nodo.padre.padre.children[0].value} # invocamos a la funcion\n")

    # Condicionales


    if nodo.Symbol_lexer == "F":
        if nodo.children:
            signo_actual = nodo.children[0].Symbol_lexer

    if nodo.Symbol_lexer == "F'":
        if nodo.children[0].Symbol_lexer == "ID" and nodo.padre.Symbol_lexer == "H":

            generar_assembly(f"\n    # e_1")
            generar_assembly(f"    la $t0, var_{nodo.children[0].value}")
            generar_assembly(f"    lw $a0, 0($t0)")

            generar_assembly(f"\n    # push")
            generar_assembly(f"    sw $a0, 0($sp)")
            generar_assembly(f"    add $sp, $sp, -4")
            
        if nodo.children[0].Symbol_lexer == "NUMERO" and nodo.padre.Symbol_lexer == "H":

            generar_assembly(f"\n    # e_2")
            generar_assembly(f"    li $a0, {nodo.children[0].value}")

            generar_assembly(f"\n    # comparacion")
            generar_assembly(f"    lw $t1, 4($sp)")
            generar_assembly(f"    add $sp, $sp, 4")

            if signo_actual == "MENOR":
                generar_assembly(f"    blt $a0, $t1, label_false\n")
            if signo_actual == "MAYOR":
                generar_assembly(f"    bgt $a0, $t1, label_false\n")
            if signo_actual == "MENOR_IGUAL":
                generar_assembly(f"    ble $a0, $t1, label_false\n")
            if signo_actual == "MAYOR_IGUAL":
                generar_assembly(f"    bge $a0, $t1, label_false\n")
            if signo_actual == "IGUAL_IGUAL":
                generar_assembly(f"    bne $a0, $t1, label_false\n")
            if signo_actual == "DIFERENTE":
                generar_assembly(f"    beq $a0, $t1, label_false\n")

            generar_assembly(f"label_true:")

    if nodo.Symbol_lexer == "ELS":
        if not nodo.children:
            generar_assembly(f"label_false:")
            generar_assembly(f"\nlabel_end:")
        else:
            generar_assembly(f"label_false:")

    if nodo.Symbol_lexer == "LLAVE_CERRADO":
        if nodo.padre.children[0].Symbol_lexer == "IF":
            generar_assembly(f"    b label_end\n")
        elif nodo.padre.children[0].Symbol_lexer == "ELSE":
            generar_assembly(f"label_end:\n")
        elif nodo.padre.Symbol_lexer == "FUNCTION":
            if nodo.padre.children[2].value == "principal":
                generar_assembly(f"\n    # Finalizar el main:")
                generar_assembly(f"    li $v0, 10")
                generar_assembly(f"    syscall ")
            else:
                generar_assembly(f"\n    lw $ra 4($sp)")
                generar_assembly(f"    addiu $sp $sp 12 # 12 = 4*num_param + 8 ")
                generar_assembly(f"    lw $fp 0($sp)")
                generar_assembly(f"    jr $ra")

    if nodo.Symbol_lexer != "PROGRAMA":
            for child in nodo.children:
                recorrer_arbol(child)

try:
    def recorrer_arbol_al_reves(nodo):
        if nodo is not None:

            for child in reversed(nodo.children):
                recorrer_arbol_al_reves(child)

        if nodo.Symbol_lexer == "FUNCTION":
            generar_assembly(f"{nodo.children[2].value}:")
            recorrer_arbol(nodo) # Desde donde se va a recorrer

    recorrer_arbol_al_reves(nodoPadre)

    with open('assembly_code.asm', 'w') as f:
        for linea in codigo_assembly:
            f.write(linea + '\n')
            print(linea)

    print(f"\nGeneración e código en ensamblador MIPS completa!!")

except TypeDataError as e:
    print(f"\nError: {e}")


