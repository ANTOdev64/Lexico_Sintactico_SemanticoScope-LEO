from sintactico import nodoPadre

def imprimir_arbol(nodo, nivel=0):
    if nodo is not None:
        print("  " * nivel + f"{nodo.Symbol_lexer}")
        for child in nodo.children:
            imprimir_arbol(child, nivel + 1)

# Llamada a la función para imprimir el árbol
imprimir_arbol(nodoPadre)
