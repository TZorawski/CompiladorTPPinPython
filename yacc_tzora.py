# Yacc
import ply.yacc as yacc
import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
 
# Get the token map from the lexer.  This is required.
from lex_tzora import tokens

count = 0

def p_programa (p):
  '''programa : lista_declaracoes'''
  global arvore

  p[0] = Node("programa", children=[p[1]])
  arvore = p[0]
  print(tabela)
  

def p_lista_declaracoes (p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao '''
    global count
    count += 1
    #print("Declaracao: " + count)
    if (len(p) == 2):
        p[0] = Node("lista_declaracoes/" + str(count), children=[p[1]])
    elif (len(p) == 3):
        p[0] = Node("lista_declaracoes/" + str(count), children=[p[1], p[2]])

def p_declaracao (p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao
    '''
    global count
    count += 1
    p[0] = Node("declaracao/" + str(count), children=[p[1]])

def p_declaracao_variaveis (p):
    '''declaracao_variaveis : tipo DOISPONTOS lista_variaveis'''
    global count
    count += 1
    p[0] = Node("declaracao_variaveis/" + str(count), children=[p[1], p[3]])
    new_line = ["VARIAVEL", p[3].children[len(p[3].children)-1].children[0].valor[0], p[1].valor[0], "", "", "", "", p.lineno(2), p.lexpos(2)]
    tabela.append(new_line)

def p_declaracao_variaveis_error (p):
    '''declaracao_variaveis : tipo DOISPONTOS error'''
    print("Erro na declaração")

def p_inicializacao_variaveis (p):
    'inicializacao_variaveis : atribuicao'
    global count
    count += 1
    p[0] = Node("inicializacao_variaveis/" + str(count), children=[p[1]])
    #p[0] = p[1]

def p_lista_variaveis (p):
    '''lista_variaveis : lista_variaveis VIRGULA var 
                       | var
    '''
    global count
    count += 1
    if (len(p) == 4):
        p[0] = Node("lista_variaveis/" + str(count), children=[p[1], p[3]])
    elif (len(p) == 2):
        p[0] = Node("lista_variaveis/" + str(count), children=[p[1]])

def p_var (p):
    '''var : ID
           | ID indice
    '''
    global count
    count += 1
    if (len(p) == 2):
        noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
        p[0] = Node("var " + p[1] + "/" + str(count), children=[noValor])
    elif (len(p) == 3):
        noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
        p[0] = Node("var/" + str(count), children=[noValor, p[2]])

def p_indice (p):
    '''indice : indice ECOLCHE expressao DCOLCHE
              | ECOLCHE expressao DCOLCHE
    '''
    global count
    count += 1
    if (len(p) == 5):
        p[0] = Node("indice/" + str(count), children=[p[1], p[3]])
    elif (len(p) == 4):
        p[0] = Node("indice/" + str(count), children=[p[2]])

def p_indice_error (p):
    '''indice : indice ECOLCHE error DCOLCHE
              | ECOLCHE error DCOLCHE
    '''
    print("Falha de indice")
    pass

def p_tipo (p):
    '''tipo : INTEIRO
            | FLUTUANTE
    '''
    global count
    count += 1
    p[0] = Node("tipo " + p[1] + "/" + str(count), valor=[p[1]])

def p_declaracao_funcao (p):
    '''declaracao_funcao : tipo cabecalho 
												 | cabecalho
    '''
    global count
    count += 1
    if (len(p) == 3):
        p[0] = Node("declaracao_funcao/" + str(count), children=[p[1], p[2]])
        new_line = ["FUNCAO", p[2].valor[0], p[1].valor[0], "", "", "", "", p.lineno(2), p.lexpos(2)]
        tabela.append(new_line)
    elif (len(p) == 2):
        p[0] = Node("declaracao_funcao/" + str(count), children=[p[1]])
        new_line = ["FUNCAO", p[1].valor[0], "void", "", "", "", "", p.lineno(1), p.lexpos(1)]
        tabela.append(new_line)

def p_cabecalho (p):
    '''cabecalho : ID EPAREN lista_parametros DPAREN corpo FIM
    '''
    global count
    count += 1
    p[0] = Node("cabecalho/" + str(count), children=[p[3], p[5]], valor=[p[1]])

def p_lista_parametros (p):
    '''lista_parametros : lista_parametros VIRGULA parametro
												| parametro
												| vazio
    '''
    global count
    count += 1
    #print("Lista variaveis: ")
    #print(len(p))
    if (len(p) == 4):
        p[0] = Node("lista_parametros/" + str(count), children=[p[1]], valor=[p[3]])
PEGAR PAI FUNCAO        new_line = ["PARAMETRO", p[1].valor[0], "void", "", "", "", "", p.lineno(1), p.lexpos(1)]
        tabela.append(new_line)
    elif (len(p) == 2):
        p[0] = Node("lista_parametros/" + str(count), valor=[p[1]])

def p_parametro (p):
    '''parametro : tipo DOISPONTOS ID
								 |  parametro ECOLCHE DCOLCHE
    '''
    global count
    count += 1
    if (p[2] == "DOISPONTOS"):
        p[0] = Node("parametro/" + str(count), children=[p[1]], valor=[p[3]])
    elif (p[2] == "ECOLCHE"):
        p[0] = Node("parametro/" + str(count), children=[p[1]])

def p_corpo (p):
    '''corpo : corpo acao 
						 | vazio
    '''
    global count
    count += 1
    if (len(p) == 3):
        p[0] = Node("corpo/" + str(count), children=[p[1], p[2]])
    elif (len(p) == 2):
        p[0] = Node("corpo/" + str(count), valor=[p[1]])

def p_acao (p):
    '''acao : expressao
						| declaracao_variaveis
						| se
						| repita
						| leia
						| escreva
						| retorna
    '''
    global count
    count += 1
    #print("ACAo")
    #print(type(p[1]))
    #print(p[1])
    if (type(p[1]) is str):
        #print("é string")
        p[0] = Node("acao " + p[1] + "/" + str(count), valor=[p[1]])
    else:
        p[0] = Node("acao/" + str(count), children=[p[1]])

def p_se (p):
    '''se : SE expressao ENTAO corpo FIM
					| SE expressao ENTAO corpo SENAO corpo FIM
    '''
    global count
    count += 1
    if (len(p) == 6):
        p[0] = Node("se/" + str(count), children=[p[2], p[4]])
    elif (len(p) == 8):
        p[0] = Node("se/" + str(count), children=[p[2], p[4], p[6]])

def p_se_error (p):
    '''se : SE error ENTAO corpo FIM
					| SE error ENTAO corpo SENAO corpo FIM
    '''
    print("Erro de expressão.")

def p_repita (p):
    '''repita : REPITA corpo ATE expressao
    '''
    global count
    count += 1
    p[0] = Node("repita/" + str(count), children=[p[2], p[4]])

def p_atribuicao (p):
    '''atribuicao : var ATRIBUICAO expressao
    '''
    global count
    count += 1
    p[0] = Node("atribuicao/" + str(count), children=[p[1], p[3]])
    new_line = ["ATRIBUICAO", p[1].children[0].valor[0], "", "", "", "", "", p.lineno(2), p.lexpos(2)]
    tabela.append(new_line)

def p_leia (p):
    '''leia : LEIA EPAREN var DPAREN
    '''
    global count
    count += 1
    p[0] = Node("leia/" + str(count), children=[p[3]])

def p_escreva (p):
    'escreva : ESCREVA EPAREN expressao DPAREN'
    global count
    count += 1
    p[0] = Node("escreva/" + str(count), children=[p[3]])

def p_retorna (p):
    '''retorna : RETORNA EPAREN expressao DPAREN
    '''
    global count
    count += 1
    p[0] = Node("retorna/" + str(count), children=[p[3]])

def p_expressao (p):
    '''expressao : expressao_logica
								 | atribuicao
    '''
    global count
    count += 1
    p[0] = Node("expressao/" + str(count), children=[p[1]])

def p_expressao_logica (p):
    '''expressao_logica : expressao_simples
												| expressao_logica operador_logico expressao_simples
    '''
    global count
    count += 1
    if (len(p) == 2):
        p[0] = Node("expressao_logica/" + str(count), children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_logica/" + str(count), children=[p[1], p[2], p[3]])

def p_expressao_simples (p):
    '''expressao_simples : expressao_aditiva
												 | expressao_simples operador_relacional expressao_aditiva
    '''
    global count
    count += 1
    if (len(p) == 2):
        p[0] = Node("expressao_simples/" + str(count), children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_simples/" + str(count), children=[p[1], p[2], p[3]])

def p_expressao_aditiva (p):
    '''expressao_aditiva : expressao_multiplicativa
												 | expressao_aditiva operador_soma expressao_multiplicativa
    '''
    global count
    count += 1
    if (len(p) == 2):
        p[0] = Node("expressao_aditiva/" + str(count), children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_aditiva/" + str(count), children=[p[1], p[2], p[3]])

def p_expressao_multiplicativa (p):
    '''expressao_multiplicativa : expressao_unaria
								| expressao_multiplicativa operador_multiplicacao expressao_unaria
    '''
    global count
    count += 1
    if (len(p) == 2):
        p[0] = Node("expressao_multiplicativa/" + str(count), children=[p[1]])
    elif (len(p) == 4):
        p[0] = Node("expressao_multiplicativa/" + str(count), children=[p[1], p[2], p[3]])

def p_expressao_unaria (p):
    '''expressao_unaria : fator
                        | operador_soma fator
                        | operador_negacao fator
    '''
    global count
    count += 1
    if (len(p) == 2):
        p[0] = Node("expressao_unaria/" + str(count), children=[p[1]])
    elif (len(p) == 3):
        p[0] = Node("expressao_unaria/" + str(count), children=[p[1], p[2]])

#??
def p_operador_relacional (p):
    '''operador_relacional : MENORQ
                            | MAIORQ 
                            | IGUAL 
                            | DESIGUAL 
                            | MENORIGUAL
                            | MAIORIGUAL
    '''
    global count
    count += 1
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
    p[0] = Node("operador_relacional " + p[1] + "/" + str(count), children=[noValor])

def p_operador_soma (p):
    '''operador_soma : ADICAO
					 | SUBTRACAO
    '''
    global count
    count += 1
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
    p[0] = Node("operador_soma/" + str(count), children=[noValor])

def p_operador_logico (p):
    '''operador_logico : ELOGICO
                        | OULOGICO
    '''
    global count
    count += 1
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
    p[0] = Node("operador_logico/" + str(count), children=[noValor])

def p_operador_negacao (p):
    '''operador_negacao : NEGACAO
    '''
    global count
    count += 1
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
    p[0] = Node("operador_negacao/" + str(count), children=[noValor])

def p_operador_multiplicacao (p):
    '''operador_multiplicacao : MULTIPLICACAO
              								| DIVISAO
    '''
    global count
    count += 1
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
    p[0] = Node("operador_multiplicacao/" + str(count), children=[noValor])

def p_fator (p):
    '''fator : EPAREN expressao DPAREN
						 | var
						 | chamada_funcao
						 | numero
    '''
    global count
    count += 1
    if (len(p) == 4):
        p[0] = Node("fator/" + str(count), children=[p[2]])
    elif (len(p) == 2):
        p[0] = Node("fator/" + str(count), children=[p[1]])

#??
def p_numero (p):
    '''numero : NUM_INTEIRO
							| NUM_FLUTUANTE
							| NUM_CIENTIFICO
    '''
    global count
    count += 1
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]])
    p[0] = Node("numero "+p[1]+" /"+str(count), children=[noValor])
		#p[0] = Node(str(p[1]))

def p_chamada_funcao (p):
    '''chamada_funcao : ID EPAREN lista_argumentos DPAREN
    '''
    global count
    count += 1
    p[0] = Node("chamada_funcao/" + str(count), children=[p[3]], valor=[p[1]])

def p_lista_argumentos (p):
    '''lista_argumentos : lista_argumentos VIRGULA expressao
												| expressao
												| vazio
    '''
    global count
    count += 1
    if (len(p) == 4):
        p[0] = Node("lista_argumentos/" + str(count), children=[p[1], p[3]])
    elif (len(p) == 2):
        p[0] = Node("lista_argumentos/" + str(count), children=[p[1]])

# Error rule for syntax errors
def p_error(p):
    #print(p)
    #print("Syntax error in input!")
    if p:
        print("Erro Sintatico: '%s' na linha '%d'" %(p.value, p.lineno-21))
        parser.errok()
    else:
        print("Erro!")

def p_vazio(p):
    '''vazio : '''
    #p[0] = Node("vazio")
    pass
    p[0] = Node("vazio/" + str(count))




arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()

arvore = Node("inicial")
tabela = [["token", "lexema", "tipo", "dimensão", "tamanho", "escopo", "inicializado", "lin", "col"]]

# Build the parser
parser = yacc.yacc()
arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()

#try:
#    s = input(data)
#except EOFError:
#    print("Erro na abertura do arquivo")

result = parser.parse(data, tracking=True)
#print(result)

# Gera grafo
#DotExporter(p[0]).to_picture("grafo.png")


