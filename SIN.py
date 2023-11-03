# Importar el nodoPadre desde el módulo sintactico_scope
from sintactico import nodoPadre

# Conjunto para almacenar funciones definidas y evitar duplicados
funcionesDefinidas = set()

# Clase para manejar errores cuando un símbolo ya está definido
class SymbolAlreadyDefinedError(Exception):
    pass

# Clase para representar la tabla de símbolos
class SymbolTable:
    def __init__(self):
        self.symbols = []  # Lista para almacenar símbolos

    def insert(self, data_type, name, scope, is_function=True):
        # Insertar un símbolo en la tabla
        symbol = {
            'data_type': data_type,
            'name': name,
            'scope': scope,
            'is_function': is_function
        }
        self.symbols.append(symbol)

    def lookup(self, name, scope):
        # Buscar un símbolo en la tabla
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

        # Recorrer los hijos del nodo actual
        for child in nodo.children:
            # Llamada recursiva para los hijos
            registrar_en_tabla(child, symbol_table, function_name if function_name else scope)

# Crear la tabla de símbolos
symbol_table = SymbolTable()

try:
    # Llamada inicial para recorrer el árbol sintáctico
    registrar_en_tabla(nodoPadre, symbol_table)

    # Imprimir la tabla de símbolos en un formato tabular
    print("\nTabla de Símbolos:")
    print("{:<10} {:<20} {:<15} {:<10}".format("Tipo", "Nombre", "Ámbito", "Flag"))
    print("-" * 60)  # Línea separadora

    for symbol in symbol_table.symbols:
        print("{:<10} {:<20} {:<15} {:<10}".format(
            symbol['data_type'], symbol['name'], symbol['scope'], "Función" if symbol['is_function'] else "Variable"
        ))

except SymbolAlreadyDefinedError as e:
    print(f"\nError: {e}")
