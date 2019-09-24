# Yacc example
"""
 ARRUMAR OPERAÇÕES DENTRO DOS IFS
"""
import ply.yacc as yacc
import sys
 
# Get the token map from the lexer.  This is required.
from lex_tzora import tokens


def programa (p):
    'programa : lista_declaracoes'
    #p[0] = p[1]

def lista_declaracoes (p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao '''
    #if (len(p) == 2):
    #    p[0] = p[1]
    #elif (len(p) == 3):
    #    p[0] = p [1] p[2]

def declaracao (p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao
    '''
    #p[0] = p[1]

def declaracao_variaveis (p):
    'declaracao_variaveis : tipo DOISPONTOS lista_variaveis'
    #p[0] = p[1] : p[3]

def inicializacao_variaveis (p):
    'inicializacao_variaveis : atribuicao'
    #p[0] = p[1]

def lista_variaveis (p):
    '''lista_variaveis : lista_variaveis "," var 
                       | var
    '''
    #if (len(p) == 4):
    #    p[0] = p[1] , p[3]
    #elif (len(p) == 2):
    #    p[0] = p[1]

def var (p):
    '''var : ID
           | ID indice
    '''
    #if (len(p) == 2):
    #    p[0] = p[1]
    #elif (len(p) == 3):
    #    p[0] = p[1] p[2]

def indice (p):
    '''indice : indice ECOLCHE expressao DCOLCHE
              | ECOLCHE expressao DCOLCHE
    '''
    #if (len(p) == 5):
    #    p[0] = p[1] [ p[3] ]
    #elif (len(p) == 4):
    #    p[0] = p [1] p [2]






# Error rule for syntax errors
def p_error(p):
   print("Syntax error in input!")

def p_vazio(p):
   'vazio :'
   #p[0] = p[2]




arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()


# Build the parser
parser = yacc.yacc()

while True:
  try:
      s = input(data)
  except EOFError:
      break
  if not s: continue
  result = parser.parse(s)
  #print(result)
