from lexico import tokens_list
from graphviz import Digraph
import pandas as pd
import math
import time


###  declaracion de valores globales


array = []
array_muerte = []
funcion = "funcion"
sub_red = []
##------------------------------------
## para que los valores sean globales de la funcion y podamos tener mas de 1 funcion
nombre = []
valor_id = []
valor_oper = []
valor_dec = []
valor_global = []


## ------------------- Declracion del Arbol

tabla_sintactica = pd.read_csv("leo_grammar.csv", index_col=0)
count = 1

print("\nIniciando analizador sintactico\n")

class nodoStack:
    def __init__(self, SymLexer, terminal):
        global count
        self.id = count
        self.SymbolLex = SymLexer
        self.terminal = terminal
        count += 1

class All_tokens:
    def __init__(self, type, lexeme, line):
        self.type = type
        self.lexeme = lexeme
        self.line = line

class nodoArbol:
    def __init__(self, Symbol_lexer, lexema, line, column, terminal, id, data_type=None, value=None):
        global count
        self.id = id
        self.lexema = lexema
        self.Symbol_lexer = Symbol_lexer
        self.terminal = terminal
        self.line = line
        self.column = column
        self.children = []
        self.padre = None
        self.symbols = []
        self.data_type = data_type
        self.value = value

    def addsymbol(self, data_type, nom_sym, function, value=None):
        Symbol_lexer = Symbol(data_type, nom_sym, function, value=value)
        self.symbols.append(Symbol_lexer)
        self.data_type = data_type
        self.value = value

class Symbol:
    def __init__(self, data_type, nom_sym, function, value=None):
        self.data_type = data_type
        self.nom_sym = nom_sym
        self.function = function
        self.value = value

class TSymbol:
    def __init__(self):
        self.symbols = []

    def insert(self, Symbol_lexer):
        self.symbols.append(Symbol_lexer)

    def lookup(self, nom_sym):
        for Symbol_lexer in self.symbols:
            if Symbol_lexer.nom_sym == nom_sym:
                return Symbol_lexer
        return None
    
Token = tokens_list

node_PROGRAMA = nodoStack("PROGRAMA", False)
node_dolar = nodoStack("$", True)
stack = [node_PROGRAMA, node_dolar]
actual_node = 1
i = 1
nodoPadre = nodoArbol("PROGRAMA", None, None, None, False, node_PROGRAMA.id)


## ------------------- pre  condiciones

class analizador:
    def __init__(self, lexema, tipo, categoria, funcion_padre, valor, line=None):
        self.lexema = lexema
        self.tipo = tipo
        self.categoria = categoria
        self.funcion_padre = funcion_padre
        self.line = line
        self.valor = valor


## -------------------- Funciones de complemento Scope ----------------

def encontrar(lexema):
    valor = False
    for symbol in array:
        print(symbol)
        for i in lexema:
            print(i)
            if symbol.lexema == i.type:
                valor = True
    return valor

## -------------------- Funciones de complemento Scope ----------------

def agregar(lexema, tipo, categoria, funcion_padre, valor):
    node_symbol = analizador(lexema, tipo, categoria, funcion_padre, valor)
    array.append(node_symbol)

## -------------------- Funciones de complemento Scope ----------------

def buscarFunciones(root):
    stack = root.children
    nombre = []
    valor_id = []
    valor_oper = []
    valor_dec = []
    nombre.append(root.children[1].lexeme)
    while len(stack) > 0:
        if stack[0].symbol.symbol == 'TERM':
            valor_id.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'OPER':
            valor_oper.append(stack[0].children[0].lexeme)
        if stack[0].symbol.symbol == 'int':
            valor_dec.append(stack[0].lexeme)
        temp = stack[0].children
        stack.pop(0)
        for i in temp:
            stack.insert(0, i)

    return valor_dec, valor_id, valor_oper, nombre



## ---------------- Funcion Scope ----------------------


def buscarVariables(root):
    print("Ayudame Gaaa", Token[1].lexeme)
    print("Ayudame Gaaa", Token[1].line)
    print("Ayudame Gaaa", Token[1].type)

        #self.id = id
        #self.lexema = lexema
        #self.Symbol_lexer = Symbol_lexer
        #self.terminal = terminal
        #self.line = line
        #self.column = column
        #self.children = []
        #self.padre = None
        #self.symbols = []
        #self.data_type = data_type
        #self.value = value

    global parametros_f, valor_f, signo_f, nombre_f
    #global valorGlobal

    # Creacion de funciones-------------------------------------------------
    #if root.symbol.symbol == "FUNCTION":
    while True:
        if encontrar(Token):
            print("FUNCION YA  CREADA -> ERROR ")
        else:
            print("FUNCION CREADA CORRECTAMENTE")
            break
            #tipo = "FUNCION"
            #categoria = None
            #padre = "LIBRE"
            #agregar(root.children[1].lexeme, tipo, categoria, padre, None)

## Aqui se recopilara toda la informacion para las funciones------------------------------------------------------------------------------------------
            parametros_f, valor_f, signo_f, nombre_f = buscarFunciones(root)
            #valorGlobal = buscarFunciones(root)
            #print(valorGlobal)
            # print(parametros_f)
            # print(valor_f)
            # print(signo_f)
            # print(nombre_f)

""""
# Creacion de variables--------------------------------------------------
    if (root.symbol.symbol == 'DECLARATION'):
        variable = root.children[1]
        nodo_tipo = root.children[0]
        expresion, valor, signo = identificado(root)
        aux = root
        # inicializarVar(variable)
        for i in (array):
            for j in range(len(valor)):
                if i.lexema == valor[j]:
                    expresion = i.categoria
        # Vamos a comprovar si esta o no es una funcion------------------
        while aux.symbol.symbol != 'FUNCTION':
            if aux.father == None:
                break
            aux = aux.father
        padre_asigando = "LIBRE"
        # tomanos el nombre de la funcion perteneciente
        # print(nodo_tipo.children[0].lexeme) 
        # print(expresion)
        if aux.symbol.symbol == 'FUNCTION':
            padre_asigando = aux.children[1].lexeme
        if encontrar(variable.lexeme):
            print("VARIABLE YA CREADA -> ERROR EN LINEA ->", variable.line)
        else:
            if nodo_tipo.children[0].lexeme == "bool" and expresion == "BOOLEAN":
                print("VARIABLE CREADA -> EN LINEA ->", variable.line)
                tipo = "id"
                categoria = expresion
                padre = padre_asigando
                agregar(variable.lexeme, tipo, categoria, padre)


            elif nodo_tipo.children[0].lexeme == "int" and expresion == "num":
                print("VARIABLE CREADA -> EN LINEA ->", variable.line)
                tipo = "id"
                categoria = expresion
                padre = padre_asigando
                convertir(variable, signo, valor)
                agregar(variable.lexeme, tipo, categoria, padre, valor)
            else:
                print("INVOCACION DE LA FUNCION -> EN LINEA ->", variable.line)

## solo soporta 1 funcion-----------------------------------------------------------------------------------------
                # print(parametros_f)
                valorG = valor_f[::-1]
                valorG = valorG[1:]
                #estos son los valores que se encuntran dentro de la funcion
                # print(valorG)
                #Esto son los signos que se encuntrar dentro de la funcion
                signo_f = signo_f[::-1]
                # print(signo_f)
                # print(nombre_f)
                # print(valor[0])
                #print("----------------")
                valor_c = valor[1:]
                valor_n = valor[:1]
                #print(valor_n)
                valor_c = valor_c[::-1]
                if nombre_f[0] == valor[0]:
                    if len(parametros_f) == len(valor_c):
                        print("Correcto -> Funcion Ejecutada")
                        invocationFuction(valor_c, variable.lexeme, valor_n )
                        createFuction(valorG, signo_f, nombre_f[0])
                    else:
                        print("Error -> En los valores ")
                else:
                    print("Error -> La funcion No fue llamada Correctamente")



                # print(variable.lexeme)
                # print(valor_c)


# Asigacion de variables-------------------------------------------------

    if root.symbol.symbol == 'ASSIGN' and root.father.symbol.symbol != 'DECLARATION' and root.father.symbol.symbol != 'FUNCTION':
        sub_valor = root.children[0]
        valor = identificado(root)
        flag = False
        for i in array:
            if i.lexema == sub_valor.lexeme and i.categoria == valor[0]:
                print('VARIABLE EN USO -> EN LINEA ->', sub_valor.line)
                flag = True
            elif i.lexema == sub_valor.lexeme and i.categoria != valor[0]:
                print('ERROR DE ASIGACION -> EN LINEA ->', sub_valor.line)
                flag = True
        if not flag:
            print('VARIABLE NO CREADA -> ERROR EN LINEA ->',  sub_valor.line)
            # return

# Deteccion de el if y el else -------------------------------------------------------

    if root.symbol.symbol == 'IF' or root.symbol.symbol == 'ELSE':

        global sub_red

        if root.symbol.symbol == 'IF':
            aux = root
            arr_valor, arr_sim, arr_id = (pack_if(root))
            arr_pack = []
            copia2 = arr_valor[:2]

            for i in range(len(array)):
                if array[i].lexema == copia2[0]:
                    arr_pack.append(copia2[i])
                    break
                else:
                    arr_pack.append(copia2[i])
                    break

            copia = arr_valor[:2]

            arr_valor1 = arr_valor[:2]
            sub_arr = arr_valor[2:]
            sup_arr = []
            arr_id = arr_id[1:]
            sub = (list(zip(sub_arr, arr_id)))
            sub_red = sub[::-1]
            flag = 0
            con = 0

            copia3 = arr_valor[:2]
            for i in range(len(copia3)):
                if copia3[i] == arr_pack[0]:
                    for t in array:
                        if copia3[i] == t.lexema:
                            copia3[i] = t.valor[0]
                            print(copia3[i])

            for j in range(len(array)):
                for i in arr_valor1:
                    if i == array[j].lexema:
                        flag += 1
                        con += 1
                    elif i.isdigit():
                        flag += 1
                        con += 1
                        sup_arr.append(i)
                    else:
                        flag += 0
                        con += 1
            stack = aux
            valor_id = []
            arr = []
            if flag >= 1:
                crearAsemblyIf(sup_arr, arr_sim, sub_red, copia, copia3)
                

        if root.symbol.symbol == 'ELSE':
            arr_valor, arr_id = (pack_else(root))
            #print(arr_valor, arr_id)

            sub_arr = arr_valor[:]
            sup_arr = []
            arr_id = arr_id[:]
            sub = (list(zip(sub_arr, arr_id)))
            sub_red1 = sub[::-1]
            deficionElse(sub_red1)
            deficionIf(sub_red)

# --------------------------------------------------------------------------------------------------------


# Eliminacion de los valores de las funciones -------------------------------------

    if root.symbol.symbol == 'fin_llave' and root.father.symbol.symbol == 'FUNCTION':
        count = 0
        for i in array:
            if i.funcion_padre == root.father.children[1].lexeme:
                count = count + 1
        while count > 0:
            for j in array:
                if j.funcion_padre == root.father.children[1].lexeme:
                    array.remove(j)
            count = count - 1

    for child in root.children:
        buscarVariables(child)
 """

#pack(root)
buscarVariables(nodoPadre)
#terminar()


#for symbol in Token:
    #print(symbol.lexeme)
        
        
        #self.id = id
        #self.lexema = lexema
        #self.Symbol_lexer = Symbol_lexer
        #self.terminal = terminal
        #self.line = line
        #self.column = column
        #self.children = []
        #self.padre = None
        #self.symbols = []
        #self.data_type = data_type
        #self.value = value