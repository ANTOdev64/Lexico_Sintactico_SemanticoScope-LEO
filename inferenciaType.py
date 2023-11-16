from sintactico import nodoPadre
from semanticoScope import symbol_table

print("\nIniciando inferencia de datos\n")

class TypeDataError(Exception):
    pass

tipo_prev = None

def verificar_compatibilidad(type_1, type_2):

    if type_1 in ["entero", "decimal"] and type_2 in ["entero", "decimal"]:
        return True
    elif type_1 == "texto" and type_2 == "texto" :
        return True

    return False


def recorrer_arbol(nodo):
    global tipo_prev
    global tipo_actual
    global scope_actual
    global tipo_scope_actual

    if nodo.Symbol_lexer == "FUNCTION":
            # Obtener información relevante
            tipo_scope_actual = nodo.children[0].children[0].children[0].value
            scope_actual = nodo.children[2].value
            print("La funcion: ", scope_actual, " es de tipo : ", tipo_scope_actual)

    elif nodo.Symbol_lexer == "Crear_variables":
        nombre_variable = nodo.children[1].value
        info_variable = symbol_table.lookup(nombre_variable, scope_actual)
        if info_variable and 'data_type' in info_variable:
            tipo_actual = info_variable['data_type']
            tipo_prev = tipo_actual
            #print(f"Según la tabla de símbolos, {nombre_variable} era de tipo {variable_actual}")

    elif nodo.Symbol_lexer == "E":
        if nodo.children[0].Symbol_lexer == "CADENA":
            nombre_variable = "texto"
            tipo_actual = nombre_variable

            print(f"Comparacion entre {tipo_prev} y {tipo_actual}")
            if tipo_prev is not None and not verificar_compatibilidad(tipo_prev, tipo_actual):
                raise TypeDataError(f"Tipos de datos incompatibles en la operación {tipo_prev} = {tipo_actual}")




    elif nodo.Symbol_lexer == "FH":

        if nodo.children[0].Symbol_lexer == "NUMERO":
            nombre_variable = "entero"
            tipo_actual = nombre_variable

            print(f"Comparacion entre {tipo_prev} y {tipo_actual}")
            if tipo_prev is not None and not verificar_compatibilidad(tipo_prev, tipo_actual):
                raise TypeDataError(f"Tipos de datos incompatibles en la operación {tipo_prev} = {tipo_actual}")


        elif nodo.children[0].Symbol_lexer == "DECIMAL":
            nombre_variable = "decimal"
            tipo_actual = nombre_variable

            print(f"Comparacion entre {tipo_prev} y {tipo_actual}")
            if tipo_prev is not None and not verificar_compatibilidad(tipo_prev, tipo_actual):
                raise TypeDataError(f"Tipos de datos incompatibles en la operación {tipo_prev} = {tipo_actual}")



        elif nodo.children[0].Symbol_lexer == "ID":
            nombre_variable = nodo.children[0].value
            info_variable = symbol_table.lookup(nombre_variable, scope_actual)
            if info_variable and 'data_type' in info_variable:
                tipo_actual = info_variable['data_type']
                #print(f"Según la tabla de símbolos, {nombre_variable} era de tipo {variable_actual}")

                print(f"Comparacion entre {tipo_prev} y {tipo_actual}")
                if tipo_prev is not None and not verificar_compatibilidad(tipo_prev, tipo_actual):
                    raise TypeDataError(f"Tipos de datos incompatibles en la operación {tipo_prev} = {tipo_actual}")
            else:
                info_variable = symbol_table.lookup(nombre_variable, "global")
                if info_variable and 'data_type' in info_variable:
                    tipo_actual = info_variable['data_type']
                    #print(f"Según la tabla de símbolos, {nombre_variable} era de tipo {variable_actual}")

                    print(f"Comparacion entre {tipo_prev} y {tipo_actual}")
                    if tipo_prev is not None and not verificar_compatibilidad(tipo_prev, tipo_actual):
                        raise TypeDataError(f"Tipos de datos incompatibles en la operación {tipo_prev} = {tipo_actual}")

    elif nodo.Symbol_lexer in ["SUMA", "RESTA", "MULTIPLICAR", "DIVIDIR"]:
        tipo_prev = tipo_actual


    elif nodo.Symbol_lexer == "PUNTO_COMA":
        tipo_prev = tipo_scope_actual
        

    for child in nodo.children:
        recorrer_arbol(child)

try:

# Llamada a la función para recorrer el árbol
    recorrer_arbol(nodoPadre)
    print(f"\nInferencia de datos correcta!!")

except TypeDataError as e:
    print(f"\nError: {e}")
