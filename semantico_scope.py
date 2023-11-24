# Importamos el nodo raíz del árbol sintáctico desde un módulo externo
from sintactico import nodoPadre

# Definimos una excepción personalizada para manejar errores de símbolos ya definidos
class SymbolAlreadyDefinedError(Exception):
    pass

# Definimos la clase SymbolTable que representa la tabla de símbolos
class SymbolTable:
    def __init__(self):
        # Inicializamos la lista de símbolos y la pila de ámbitos con el ámbito global
        self.symbols = []
        self.scope_stack = ["global"]

    def enter_scope(self, scope):
        # Función para ingresar a un nuevo ámbito
        self.scope_stack.append(scope)

    def exit_scope(self):
        # Función para salir del ámbito actual
        self.scope_stack.pop()

    def get_current_scope(self):
        # Función para obtener el ámbito actual
        return self.scope_stack[-1]

    def insert(self, data_type, name, is_function=True):
        # Función para insertar un nuevo símbolo en la tabla
        symbol = {
            'data_type': data_type,
            'name': name,
            'scope': self.get_current_scope() if not is_function else "global",
            'is_function': is_function
        }
        self.symbols.append(symbol)

    def lookup(self, name):
        # Función para buscar un símbolo en la tabla
        for symbol in reversed(self.symbols):
            if symbol['name'] == name and symbol['scope'] in self.scope_stack:
                return symbol
        return None

# Función recursiva para recorrer el árbol sintáctico y registrar funciones, variables y parámetros en la tabla de símbolos
def registrar_en_tabla(nodo, symbol_table):
    if nodo is not None:
        if nodo.Symbol_lexer == "FUNCTION":
            # Si el nodo representa una función, obtenemos el tipo, el nombre y entramos a un nuevo ámbito
            type_node = nodo.children[0].children[0].children[0].value
            function_name = nodo.children[2].value
            symbol_table.enter_scope(function_name)
            symbol_table.insert(type_node, function_name, is_function=True)

        elif nodo.Symbol_lexer == "TI":
            # Si el nodo representa un tipo (parámetro o variable), obtenemos el tipo y el nombre
            type_node = nodo.children[0].children[0].children[0].value if len(nodo.children) > 0 and len(
                nodo.children[0].children) > 0 and len(nodo.children[0].children[0].children) > 0 else None
            parameter_name = nodo.children[1].value if len(nodo.children) > 1 else None
            # Verificamos si el símbolo ya está definido en el ámbito actual
            if type_node and parameter_name:
                existing_symbol = symbol_table.lookup(parameter_name)
                if existing_symbol:
                    raise SymbolAlreadyDefinedError(
                        f"El parámetro '{parameter_name}' ya estaba definido en el ámbito '{symbol_table.get_current_scope()}'")
                else:
                    # Insertamos el nuevo símbolo en la tabla
                    symbol_table.insert(type_node, parameter_name, is_function=False)

        elif nodo.Symbol_lexer == "Crear_variables" and len(nodo.children) >= 2:
            # Si el nodo representa la creación de variables, obtenemos el tipo y el nombre
            type_node = nodo.children[0].children[0].children[0].value if len(nodo.children[0].children) > 0 and len(
                nodo.children[0].children[0].children) > 0 else None
            variable_name = nodo.children[1].value if len(nodo.children) > 1 else None
            # Verificamos si la variable ya está definida en el ámbito actual
            if type_node and variable_name:
                existing_symbol = symbol_table.lookup(variable_name)
                if existing_symbol:
                    raise SymbolAlreadyDefinedError(
                        f"La variable '{variable_name}' ya estaba definida en el ámbito '{symbol_table.get_current_scope()}'")
                else:
                    # Insertamos la nueva variable en la tabla
                    symbol_table.insert(type_node, variable_name, is_function=False)

        for child in nodo.children:
            # Llamada recursiva para procesar los hijos del nodo actual
            registrar_en_tabla(child, symbol_table)

        if nodo.Symbol_lexer == "FUNCTION":
            # Si el nodo es una función, salimos del ámbito actual
            symbol_table.exit_scope()

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
        # Imprimir cada símbolo en la tabla
        print("{:<10} {:<20} {:<15} {:<10}".format(
            symbol['data_type'], symbol['name'], symbol['scope'], "Función" if symbol['is_function'] else "Variable"
        ))

except SymbolAlreadyDefinedError as e:
    # Capturar y manejar excepciones de símbolos ya definidos
    print(f"\nError: {e}")
