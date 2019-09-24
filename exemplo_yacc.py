# Yacc example
"""
 ARRUMAR OPERAÇÕES DENTRO DOS IFS
"""
import ply.yacc as yacc
import sys
 
# Get the token map from the lexer.  This is required.
from lex_tzora import tokens


def p_programa (p):
    'programa : lista_declaracoes'
    #p[0] = p[1]

def p_lista_declaracoes (p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao '''
    #if (len(p) == 2):
    #    p[0] = p[1]
    #elif (len(p) == 3):
    #    p[0] = p [1] p[2]

def p_declaracao (p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao
    '''
    #p[0] = p[1]

def p_declaracao_variaveis (p):
    'declaracao_variaveis : tipo DOISPONTOS lista_variaveis'
    #p[0] = p[1] : p[3]

def p_inicializacao_variaveis (p):
    'inicializacao_variaveis : atribuicao'
    #p[0] = p[1]

def p_lista_variaveis (p):
    '''lista_variaveis : lista_variaveis "," var 
                       | var
    '''
    #if (len(p) == 4):
    #    p[0] = p[1] , p[3]
    #elif (len(p) == 2):
    #    p[0] = p[1]

def p_var (p):
    '''var : ID
           | ID indice
    '''
    #if (len(p) == 2):
    #    p[0] = p[1]
    #elif (len(p) == 3):
    #    p[0] = p[1] p[2]

def p_indice (p):
    '''indice : indice ECOLCHE expressao DCOLCHE
              | ECOLCHE expressao DCOLCHE
    '''
    #if (len(p) == 5):
    #    p[0] = p[1] [ p[3] ]
    #elif (len(p) == 4):
    #    p[0] = p [1] p [2]

def p_tipo (p):
    '''tipo : INTEIRO
              | FLUTUANTE
    '''

def p_declaracao_funcao (p):
    '''declaracao_funcao : tipo cabecalho 
												 | cabecalho
    '''

def p_cabecalho (p):
    '''cabecalho : ID EPAREN lista_parametros DPAREN corpo FIM
    '''

def p_lista_parametros (p):
    '''lista_parametros : lista_parametros VIRGULA parametro
												| parametro
												| vazio
    '''

def p_parametro (p):
    '''parametro : tipo DOISPONTOS ID
								 |  parametro ECOLCHE DCOLCHE
    '''

def p_corpo (p):
    '''corpo : corpo acao 
						 | vazio
    '''

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

def p_se (p):
    '''se : SE expressao ENTAO corpo FIM
					| SE expressao ENTAO corpo SENAO corpo FIM
    '''

def p_repita (p):
    '''repita : REPITA corpo ATE expressao
    '''

def p_atribuicao (p):
    '''atribuicao : var ATRIBUICAO expressao
    '''

def p_leia (p):
    '''leia : LEIA EPAREN var DPAREN
    '''

def p_escreva (p):
    '''escreva : ESCREVA EPAREN expressao DPAREN
    '''

def p_retorna (p):
    '''retorna : RETORNA EPAREN expressao DPAREN
    '''

def p_expressao (p):
    '''expressao : expressao_logica
								 | atribuicao
    '''

def p_expressao_logica (p):
    '''expressao_logica : expressao_simples
												| expressao_logica operador_logico expressao_simples
    '''

def p_expressao_simples (p):
    '''expressao_simples : expressao_aditiva
												 | expressao_simples operador_relacional expressao_aditiva
    '''

def p_expressao_aditiva (p):
    '''expressao_aditiva : expressao_multiplicativa
												 | expressao_aditiva operador_soma expressao_multiplicativa
    '''

def p_expressao_multiplicativa (p):
    '''expressao_multiplicativa : expressao_unaria
																| expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''

def p_expressao_unaria (p):
    '''expressao_unaria : fator
												| operador_soma fator
												| operador_negacao fator
    '''

def p_operador_relacional (p):
    '''operador_relacional : MENORQ
													 | MAIORQ 
													 | IGUAL 
													 | DESIGUAL 
													 | MENORIGUAL
													 | MAIORIGUAL
    '''

def p_operador_soma (p):
    '''operador_soma : ADICAO
										 | SUBTRACAO
    '''

def p_operador_logico (p):
    '''operador_logico : ELOGICO
											 | OULOGICO
    '''

def p_operador_negacao (p):
    '''operador_negacao : NEGACAO
    '''

def p_operador_multiplicacao (p):
    '''operador_multiplicacao : MULTIPLICACAO
              								| DIVISAO
    '''

def p_fator (p):
    '''fator : EPAREN expressao DPAREN
						 | var
						 | chamada_funcao
						 | numero
    '''

def p_numero (p):
    '''numero : NUM_INTEIRO
							| NUM_FLUTUANTE
							| NUM_CIENTIFICO
    '''

def p_chamada_funcao (p):
    '''chamada_funcao : ID EPAREN lista_argumentos DPAREN
    '''

def p_lista_argumentos (p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
												| expressao
												| vazio
    '''

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

try:
    s = input(data)
except EOFError:
    print("Erro na abertura do arquivo")

result = parser.parse(s)
