import os

# Ruta al ejecutable dot de Graphviz
os.environ["PATH"] += os.pathsep + r'C:\Graphviz\bin'


from lexico import tokens_list
from graphviz import Digraph
import pandas as pd
import math
import time

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

symbols = []
# Verifiar el search
def Search(node, id):
      if node.id == id:
          return node
      for c in node.children:
          found_node = Search(c, id)
          if found_node is not None:
              return found_node
      return None

def arbolSintactico(root):
      dot = Digraph()

      def generar_nodos(node):

          label = f"{node.Symbol_lexer}"
          if node.line is not None:
              label += f"\nline: {node.line}"
          if node.column is not None:
            label += f"\ncol: {node.column}"
          if node.value is not None:
              label += f"\nvalue: {node.value}"

          dot.node(str(node.id), label, style="filled", fillcolor='white')
          
          if node.padre:
              dot.edge(str(node.padre.id), str(node.id))

          for child in node.children:
              generar_nodos(child)

      generar_nodos(root)
      print("Generando arbol sintactico")
      word = ""

      for punto in range(3):
          print(word[:punto+1], end='', flush=True)
          time.sleep(1)
          print(".", end='', flush=True)
          time.sleep(1)

      time.sleep(1)
      dot.render('arbolSintactico', format='png', view=False)

error = False
n = 0
t = []

for tkk in Token:
      t.append(tkk)
  
while True:
      if stack[0].SymbolLex == "$" and Token[0].type == "$":
          print("Sintaxis correcta!!")
          break

      elif stack[0].terminal and stack[0].SymbolLex == Token[0].type:
          stack.pop(0)
          token = Token.pop(0)
          data_type = Token[0].type
          if data_type is not None:
              padre = Search(nodoPadre, actual_node)
              padre.data_type = data_type

      elif stack[0].terminal and stack[0].SymbolLex != Token[0].type:
          print("ERROR sintáctico!!")
          error = True
          break
      else:
          prod = tabla_sintactica.loc[stack[0].SymbolLex][Token[0].type]

          if prod == "e":
              stack.pop(0)
          else:
              if isinstance(prod, float) and math.isnan(prod):
                  print("ERROR sintáctico!!")
                  error = True
                  break
              else:
                  prod = prod.split(" ")
                  padre_stack = stack.pop(0)

                  # verifica que devuelve un nodeArbol
                  padre = Search(nodoPadre, padre_stack.id)
                  

                  for Symlexer in prod[::-1]:
                    is_terminal = Symlexer in tabla_sintactica.columns
                    node = nodoStack(Symlexer, is_terminal)
                    stack.insert(0, node)
                    actual_node = node.id
                    
                    nod = nodoArbol(Symlexer, None, None, None, is_terminal, node.id)

                    
                    padre.children.insert(0, nod)
                    nod.padre = padre

                    
                    if nod.terminal:
                      for tkk in t:
                        if tkk.type == nod.Symbol_lexer:
                          nod.value = tkk.lexeme
                          nod.line = tkk.line
                          nod.column = tkk.column
                          t.remove(tkk)
                          break
      
if (error == False):
    arbolSintactico(nodoPadre)