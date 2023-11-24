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
        generar_assembly(f"    {symbol['name']}: .word 0")


codigo_assembly.append(".text")

codigo_assembly.append("main:")

t_count = -1

tipo_prev = None

def recorrer_arbol(nodo):
    global tipo_prev
    global tipo_actual
    global scope_actual
    global tipo_scope_actual
    global t_count

    global variable_actual
    

    if nodo.Symbol_lexer == "FUNCTION":
        tipo_scope_actual = nodo.children[0].children[0].children[0].value
        scope_actual = nodo.children[2].value

    elif nodo.Symbol_lexer == "Crear_variables":
        variable_actual = nodo.children[1].value
    # LUEGO DEL IGUAL =

    elif nodo.Symbol_lexer == "E":
        if nodo.children[0].Symbol_lexer == "CADENA":
            nombre_variable = nodo.children[0].value
            tipo_actual = nombre_variable

    elif nodo.Symbol_lexer == "FH":
        if nodo.children[0].Symbol_lexer == "NUMERO":
            nombre_variable = nodo.children[0].value
            tipo_actual = nombre_variable
            t_count += 1
            generar_assembly(f"    li $t{t_count}, {nodo.children[0].value}")

        elif nodo.children[0].Symbol_lexer == "DECIMAL":
            nombre_variable = nodo.children[0].value
            tipo_actual = nombre_variable

        elif nodo.children[0].Symbol_lexer == "ID":
            nombre_variable = nodo.children[0].value
            info_variable = symbol_table.lookup(nombre_variable, scope_actual)
            if info_variable and 'data_type' in info_variable:
                tipo_actual = info_variable['data_type']
            else:
                info_variable = symbol_table.lookup(nombre_variable, "global")
                if info_variable and 'data_type' in info_variable:
                    tipo_actual = info_variable['data_type']

    elif nodo.Symbol_lexer in ["SUMA", "RESTA", "MULTIPLICAR", "DIVIDIR"]:
        tipo_prev = tipo_actual
        if nodo.padre.padre.Symbol_lexer != "E":
            if nodo.Symbol_lexer == "SUMA":
                t_count += 1
                agrear_pila(f"    add $t{t_count}, $t{max(0, t_count-2)}, $t{t_count+1}")
            if nodo.Symbol_lexer == "RESTA":
                t_count += 1
                agrear_pila(f"    sub $t{t_count}, $t{max(0, t_count-2)}, $t{t_count+1}")
            if nodo.Symbol_lexer == "MULTIPLICAR":
                t_count += 1
                agrear_pila(f"    mult $t{max(0, t_count-2)}, $t{t_count+1}")
                agrear_pila(f"    mflo $t{t_count}")
            if nodo.Symbol_lexer == "DIVIDIR":
                t_count += 1
                agrear_pila(f"    div $t{max(0, t_count-2)}, $t{t_count+1}")
                agrear_pila(f"    mflo $t{t_count}")
        else:
            if nodo.Symbol_lexer == "SUMA":
                t_count += 1
                agrear_pila(f"    add $t{t_count}, $t{max(0, t_count-1)}, $t{t_count+1}")
            if nodo.Symbol_lexer == "RESTA":
                t_count += 1
                agrear_pila(f"    sub $t{t_count}, $t{max(0, t_count-1)}, $t{t_count+1}")
            if nodo.Symbol_lexer == "MULTIPLICAR":
                t_count += 1
                agrear_pila(f"    mult $t{max(0, t_count-1)}, $t{t_count+1}")
                agrear_pila(f"    mflo $t{t_count}")
            if nodo.Symbol_lexer == "DIVIDIR":
                t_count += 1
                agrear_pila(f"    div $t{max(0, t_count-1)}, $t{t_count+1}")
                agrear_pila(f"    mflo $t{t_count}")



    elif nodo.Symbol_lexer == "PUNTO_COMA":
        if nodo.padre.children[0].Symbol_lexer == "Crear_variables":
            tipo_prev = tipo_scope_actual
            generar_assembly(f"")

            for exp in pila_expresion:
                generar_assembly(exp)

            generar_assembly(f"    sw $t{max(0, t_count-1)}, {variable_actual}")
            t_count += 1

    elif nodo.Symbol_lexer == "ID":
        if nodo.padre.Symbol_lexer == "TX":
            generar_assembly(f"\n    # Imprimir {nodo.value}:")
            generar_assembly(f"    lw $a0, {nodo.value}")
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
