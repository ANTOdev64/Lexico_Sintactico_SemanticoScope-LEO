import math
from sintactico import nodoPadre
from semanticoScope import symbol_table

print("\nIniciando generación de código en ensamblador MIPS\n")

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
    if symbol['is_function'] == False and symbol['data_type'] == "entero":
        generar_assembly(f"    var_{symbol['name']}: .word 0:1")


codigo_assembly.append(".text")

codigo_assembly.append("main:")

acum_pila = True

tipo_prev = None

op_actual = []
bypass = False

def recorrer_arbol(nodo):
    global tipo_prev
    global tipo_actual
    global scope_actual
    global tipo_scope_actual


    global acum_pila
    global variable_actual
    global op_actual
    global bypass

    
    

    if nodo.Symbol_lexer == "FUNCTION":
        tipo_scope_actual = nodo.children[0].children[0].children[0].value
        scope_actual = nodo.children[2].value

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
            if nodo.padre.Symbol_lexer != "E" and bypass == True:
                generar_assembly(f"\n    lw $t1 4($sp) # Del de la pila al temporal")
                generar_assembly(op_actual[0])
                if len(op_actual) > 1:
                    generar_assembly(op_actual[1])
                generar_assembly(f"    add $sp $sp 4 # POP")

                acum_pila = True
            bypass = True

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
                bypass = True
                acum_pila = True
        
    if nodo.Symbol_lexer == "E'":
        if not nodo.children:
            tipo_prev = tipo_scope_actual
            generar_assembly(f"")

            generar_assembly(f"    la  $t1, var_{variable_actual}")
            generar_assembly(f"    sw  $a0, 0($t1)\n")

    elif nodo.Symbol_lexer == "ID":
        if nodo.padre.Symbol_lexer == "TX":
            generar_assembly(f"\n    # Imprimir {nodo.value}:")
            generar_assembly(f"    lw $a0, var_{nodo.value}")
            generar_assembly(f"    li $v0, 1")
            generar_assembly(f"    syscall")

    for child in nodo.children:
        recorrer_arbol(child)

try:
    recorrer_arbol(nodoPadre)

    generar_assembly(f"\n    # Finalizar el main:")
    generar_assembly(f"    li $v0, 10  ")
    generar_assembly(f"    syscall ")

    with open('assembly_code.asm', 'w') as f:
        for linea in codigo_assembly:
            f.write(linea + '\n')
            print(linea)

    print(f"\nGeneración de código en ensamblador MIPS completa!!")

except TypeDataError as e:
    print(f"\nError: {e}")
