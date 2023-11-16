# Importar el nodoPadre desde el módulo sintactico_scope
from sintactico import nodoPadre

print("\n")

funcionesDefinidas = set()

class SymbolAlreadyDefinedError(Exception):
    pass

class UndefinedVariableError(Exception):
    pass

class SymbolTable:
    def __init__(self):
        self.symbols = []

    def insert(self, data_type, name, scope, is_function=True):
        symbol = {
            'data_type': data_type,
            'name': name,
            'scope': scope,
            'is_function': is_function
        }
        self.symbols.append(symbol)

    def lookup(self, name, scope):
        for symbol in self.symbols:
            if symbol['name'] == name and symbol['scope'] == scope:
                return symbol
        return None

# Función recursiva para recorrer el árbol sintáctico y registrar funciones, variables y parámetros en la tabla de símbolos
def registrar_en_tabla(nodo, symbol_table, scope="global"):
    function_name = None  # Inicializamos function_name aquí

    if nodo is not None:
        # Verificar si el nodo representa una función
        if nodo.Symbol_lexer == "FUNCTION":
            # Obtener información relevante
            type_node = nodo.children[0].children[0].children[0].value
            function_name = nodo.children[2].value
            # Insertar en la tabla de símbolos
            if function_name in funcionesDefinidas:
                raise SymbolAlreadyDefinedError(f"La función '{function_name}' ya estaba definida")
            else:
                funcionesDefinidas.add(function_name)
                symbol_table.insert(type_node, function_name, "global")

        # Verificar si el nodo representa parámetros
        elif nodo.Symbol_lexer == "TI":
            # Obtener información relevante
            type_node = nodo.children[0].children[0].children[0].value if len(nodo.children) > 0 and len(nodo.children[0].children) > 0 and len(nodo.children[0].children[0].children) > 0 else None
            parameter_name = nodo.children[1].value if len(nodo.children) > 1 else None
            # Insertar en la tabla de símbolos
            if type_node and parameter_name:
                existing_symbol = symbol_table.lookup(parameter_name, scope)
                if existing_symbol:
                    raise SymbolAlreadyDefinedError(f"El parámetro '{parameter_name}' ya estaba definido en el ámbito '{scope}'")
                else:
                    symbol_table.insert(type_node, parameter_name, scope, is_function=False)

        # Verificar si el nodo representa la creación de variables
        elif nodo.Symbol_lexer == "Crear_variables" and len(nodo.children) >= 2:
            # Obtener información relevante
            type_node = nodo.children[0].children[0].children[0].value if len(nodo.children[0].children) > 0 and len(nodo.children[0].children[0].children) > 0 else None
            variable_name = nodo.children[1].value if len(nodo.children) > 1 else None
            # Insertar en la tabla de símbolos
            existing_symbol = symbol_table.lookup(variable_name, scope)
            if existing_symbol:
                raise SymbolAlreadyDefinedError(f"La variable '{variable_name}' ya estaba definida en el ámbito '{scope}'")
            else:
                symbol_table.insert(type_node, variable_name, scope, is_function=False)

        # Verifica las variables despues del = id + id;  SE DEBE VERIFICAR SI YA SE DEFINIÓ LA VARIABLE
        elif nodo.Symbol_lexer == "FH":

            try:
                if nodo.children[0].Symbol_lexer == "ID" and nodo.children[1].children[0].Symbol_lexer == "PARENTESIS_ABIERTO": # SE DEBE VERIFICAR SI YA SE DEFINIÓ LA FUNCION
                    #print("Funcion: ",nodo.children[0].value)
                    function_name2 = nodo.children[0].value
                    existing_symbol = symbol_table.lookup(function_name2, "global")
                    if not existing_symbol:
                        raise UndefinedVariableError
                    
            except UndefinedVariableError as e:
                raise UndefinedVariableError(f"La función '{function_name2}' no estaba definida en el ámbito 'global'")


            except Exception as e: 
                if nodo.children[0].Symbol_lexer == "ID": # SE DEBE VERIFICAR SI YA SE DEFINIÓ LA VARIABLE
                    #print("Variable: ", nodo.children[0].value)
                    variable_name = nodo.children[0].value
                    existing_symbol = symbol_table.lookup(variable_name, scope)
                    if not existing_symbol:
                        raise UndefinedVariableError(f"La variable '{variable_name}' no estaba definida en el ámbito '{scope}'")

        # Verifica las variables después del = id (id, id); SE DEBE VERIFICAR SI YA SE DEFINIÓ LA FUNCION
        elif nodo.Symbol_lexer == "F'":
            if nodo.children[0].Symbol_lexer == "ID":
                #print("Variable: ", nodo.children[0].value)
                variable_name = nodo.children[0].value
                existing_symbol = symbol_table.lookup(variable_name, scope)
                if not existing_symbol:
                    raise UndefinedVariableError(f"La variable '{variable_name}' no estaba definida en el ámbito '{scope}'")


        # Verifica las variables despues del imprimir (id, id);  SE DEBE VERIFICAR SI YA SE DEFINIÓ LA VARIABLE
        elif nodo.Symbol_lexer == "TX":
            if nodo.children[0].Symbol_lexer == "ID":
                #print("Variable: ", nodo.children[0].value)
                variable_name = nodo.children[0].value
                existing_symbol = symbol_table.lookup(variable_name, scope)
                if not existing_symbol:
                    raise UndefinedVariableError(f"La variable '{variable_name}' no estaba definida en el ámbito '{scope}'")

        elif nodo.Symbol_lexer == "sentencia":
            if nodo.children[1].Symbol_lexer == "ID":
                #print("Variable: ", nodo.children[1].value)
                variable_name = nodo.children[1].value
                existing_symbol = symbol_table.lookup(variable_name, scope)
                if not existing_symbol:
                    raise UndefinedVariableError(f"La variable '{variable_name}' no estaba definida en el ámbito '{scope}'")


        # Recorrer los hijos del nodo actual
        for child in nodo.children:
            # Llamada recursiva para los hijos
            registrar_en_tabla(child, symbol_table, function_name if function_name else scope)

# Crear la tabla de símbolos
symbol_table = SymbolTable()

try:
    # Llamada inicial para recorrer el árbol sintáctico
    registrar_en_tabla(nodoPadre, symbol_table)

    print("\nTabla de Símbolos:")
    print(f"{'Tipo':<10} | {'Nombre':<15} | {'Ámbito':<15} | {'Función':<10}")
    print("-" * 60)
    for symbol in symbol_table.symbols:
        data_type = symbol['data_type']
        name = symbol['name']
        scope = symbol['scope']
        is_function = "Función" if symbol['is_function'] else "Variable"
        print(f"{data_type:<10} | {name:<15} | {scope:<15} | {is_function:<10}")


except SymbolAlreadyDefinedError as e:
    print(f"\nError: {e}")

except UndefinedVariableError as e:
    print(f"\nError: {e}")