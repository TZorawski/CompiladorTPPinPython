# Yacc example
"""
 ARRUMAR OPERAÇÕES DENTRO DOS IFS
"""
import ply.yacc as yacc
import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
 
# Get the token map from the lexer.  This is required.
from lex_tzora import tokens


def p_programa (p):
	'''programa : lista_declaracoes'''
	p[0] = Node("programa", children=[p[1]])
	# Gera grafo
	DotExporter(p[0]).to_picture("grafo2.png")

def p_lista_declaracoes (p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao '''
    if (len(p) == 2):
        p[0] = Node("lista_declaracoes", children=[p[1]])
    elif (len(p) == 3):
        p[0] = Node("lista_declaracoes", children=[p[1], p[2]])

def p_declaracao (p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao
    '''
    p[0] = Node("declaracao", children=[p[1]])

def p_declaracao_variaveis (p):
    '''declaracao_variaveis : tipo DOISPONTOS lista_variaveis'''
    p[0] = Node("declaracao_variaveis", children=[p[1], p[3]])

def p_inicializacao_variaveis (p):
    'inicializacao_variaveis : atribuicao'
    p[0] = Node("inicializacao_variaveis", children=[p[1]])
    #p[0] = p[1]

def p_lista_variaveis (p):
    '''lista_variaveis : lista_variaveis "," var 
                       | var
    '''
    if (len(p) == 4):

        p[0] = Node("lista_variaveis", children=[p[1], p[3]])
    elif (len(p) == 2):
        p[0] = Node("lista_variaveis", children=[p[1]])

def p_var (p):
    '''var : ID
           | ID indice
    '''
    if (len(p) == 2):
        p[0] = Node("var", children=[p[1]])
    elif (len(p) == 3):
        p[0] = Node("var", children=[p[1], p[2]])

def p_indice (p):
    '''indice : indice ECOLCHE expressao DCOLCHE
              | ECOLCHE expressao DCOLCHE
    '''
    if (len(p) == 5):
        p[0] = Node("indice", children=[p[1], p[3]])
    elif (len(p) == 4):
        p[0] = Node("indice", children=[p[2]])

def p_tipo (p):
    '''tipo : INTEIRO
              | FLUTUANTE
    '''
    p[0] = Node("tipo", children=[p[1]])

def p_declaracao_funcao (p):
    '''declaracao_funcao : tipo cabecalho 
												 | cabecalho
    '''
    p[0] = Node("declaracao_funcao", children=[p[1]])

def p_cabecalho (p):
    '''cabecalho : ID EPAREN lista_parametros DPAREN corpo FIM
    '''
    p[0] = Node("cabecalho", children=[p[1], p[3], p[5]])

def p_lista_parametros (p):
    '''lista_parametros : lista_parametros VIRGULA parametro
												| parametro
												| vazio
    '''
    if (len(p) == 4):
        p[0] = Node("lista_parametros", children=[p[1], p[3]])
    elif (len(p) == 2):
        p[0] = Node("lista_parametros", children=[p[1]])

def p_parametro (p):
    '''parametro : tipo DOISPONTOS ID
								 |  parametro ECOLCHE DCOLCHE
    '''
    if (p[2] == "DOISPONTOS"):
        p[0] = Node("parametro", children=[p[1], p[3]])
    elif (p[2] == "ECOLCHE"):
        p[0] = Node("parametro", children=[p[1]])

def p_corpo (p):
    '''corpo : corpo acao 
						 | vazio
    '''
    if (len(p) == 3):
        p[0] = Node("corpo", children=[p[1], p[3]])
    elif (len(p) >= 1):
        p[0] = Node("corpo", children=[p[1]])

def p_acao (p):
    '''acao : expressao
						| declaracao_variaveis
						| SE
						| REPITA
						| LEIA
						| ESCREVA
						| RETORNA
						| error
    '''
    p[0] = Node("acao", children=[p[1]])

def p_se (p):
    '''se : SE expressao ENTAO corpo FIM
					| SE expressao ENTAO corpo SENAO corpo FIM
    '''
    if (len(p) == 6):
        p[0] = Node("se", children=[p[2], p[4]])
    elif (len(p) == 8):
        p[0] = Node("se", children=[p[2], p[4], p[6]])

def p_repita (p):
    '''repita : REPITA corpo ATE expressao
    '''
    p[0] = Node("repita", children=[p[2], p[4]])

def p_atribuicao (p):
    '''atribuicao : var ATRIBUICAO expressao
    '''
    p[0] = Node("atribuicao", children=[p[1], p[3]])

def p_leia (p):
    '''leia : LEIA EPAREN var DPAREN
    '''
    p[0] = Node("leia", children=[p[3]])

def p_escreva (p):
    '''escreva : ESCREVA EPAREN expressao DPAREN
    '''
    p[0] = Node("escreva", children=[p[3]])

def p_retorna (p):
    '''retorna : RETORNA EPAREN expressao DPAREN
    '''
    p[0] = Node("retorna", children=[p[3]])

def p_expressao (p):
    '''expressao : expressao_logica
								 | atribuicao
    '''
    p[0] = Node("expressao", children=[p[1]])

def p_expressao_logica (p):
    '''expressao_logica : expressao_simples
												| expressao_logica operador_logico expressao_simples
    '''
    if (len(p) == 2):
        p[0] = Node("expressao_logica", children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_logica", children=[p[1], p[2], p[3]])

def p_expressao_simples (p):
    '''expressao_simples : expressao_aditiva
												 | expressao_simples operador_relacional expressao_aditiva
    '''
    if (len(p) == 2):
        p[0] = Node("expressao_simples", children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_simples", children=[p[1], p[2], p[3]])

def p_expressao_aditiva (p):
    '''expressao_aditiva : expressao_multiplicativa
												 | expressao_aditiva operador_soma expressao_multiplicativa
    '''
    if (len(p) == 2):
        p[0] = Node("expressao_aditiva", children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_aditiva", children=[p[1], p[2], p[3]])

def p_expressao_multiplicativa (p):
    '''expressao_multiplicativa : expressao_unaria
								| expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''
    if (len(p) == 2):
        p[0] = Node("expressao_multiplicativa", children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_multiplicativa", children=[p[1], p[2], p[3]])

def p_expressao_unaria (p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator
    '''
    if (len(p) == 2):
        p[0] = Node("expressao_unaria", children=[p[1]])
    elif (len(p) == 3):
        p[0] = Node("expressao_unaria", children=[p[1], p[2]])

#??
def p_operador_relacional (p):
    '''operador_relacional : MENORQ
                            | MAIORQ 
                            | IGUAL 
                            | DESIGUAL 
                            | MENORIGUAL
                            | MAIORIGUAL
    '''
    p[0] = Node("operador_relacional", children=[p[1]])

def p_operador_soma (p):
    '''operador_soma : ADICAO
					 | SUBTRACAO
    '''
    p[0] = Node("operador_soma", children=[p[1]])

def p_operador_logico (p):
    '''operador_logico : ELOGICO
                        | OULOGICO
    '''
    p[0] = Node("operador_logico", children=[p[1]])

def p_operador_negacao (p):
    '''operador_negacao : NEGACAO
    '''
    p[0] = Node("operador_negacao", children=[p[1]])

def p_operador_multiplicacao (p):
    '''operador_multiplicacao : MULTIPLICACAO
              								| DIVISAO
    '''
    p[0] = Node("operador_multiplicacao", children=[p[1]])

def p_fator (p):
    '''fator : EPAREN expressao DPAREN
						 | var
						 | chamada_funcao
						 | numero
    '''
    if (len(p) == 4):
        p[0] = Node("fator", children=[p[2]])
    elif (len(p) == 2):
        p[0] = Node("fator", children=[p[1]])

#??
def p_numero (p):
    '''numero : NUM_INTEIRO
							| NUM_FLUTUANTE
							| NUM_CIENTIFICO
    '''
    p[0] = Node("numero", children=[p[1]])
		#p[0] = Node(str(p[1]))

def p_chamada_funcao (p):
    '''chamada_funcao : ID EPAREN lista_argumentos DPAREN
    '''
    p[0] = Node("chamada_funcao", children=[p[1], p[3]])

def p_lista_argumentos (p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
												| expressao
												| vazio
    '''
    if (len(p) == 4):
        p[0] = Node("lista_argumentos", children=[p[1], p[3]])
    elif (len(p) == 2):
        p[0] = Node("lista_argumentos", children=[p[1]])

# Error rule for syntax errors
def p_erro(p):
    print("Syntax error in input!")

def p_vazio(p):
    'vazio :'
    #p[0] = p[2]




arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()


# Build the parser
parser = yacc.yacc()
arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()

#try:
#    s = input(data)
#except EOFError:
#    print("Erro na abertura do arquivo")

result = parser.parse(data)
print(result)


