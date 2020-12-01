# Yacc
import ply.yacc as yacc
import sys
from anytree import Node, RenderTree
from anytree.exporter import DotExporter
 
# Get the token map from the lexer.  This is required.
from lex_tzora import tokens

count = 0
tem_erro_yacc = False

def p_programa (p):
  '''programa : lista_declaracoes'''
  global arvore

  p[0] = Node("programa", children=[p[1]])
  arvore = p[0]

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
    #elimina variaveis globais do vetor de variaveis
    global variaveis
    variaveis = []

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
    no_atual = p[3]

    #adiciona todas as variáveis da lista de variaveis na tabela
    var_a_percorrer = len(p[3].leaves)
    global tem_erro_yacc
    while(var_a_percorrer != 0 and (not tem_erro_yacc)):
        new_line = ["VARIAVEL", no_atual.children[len(no_atual.children)-1].children[0].valor[0], p[1].valor[0], "", "", "global", 0, 0, "", p.lineno(2), p.lexpos(2)]
        tabela.append(new_line)
        variaveis.append( len(tabela)-1 )
        # --- guarda no atributo "tipo" do nó de valor do nó "var" o tipo da variável, para facilitar futuras computações ---
        no_atual.children[len(no_atual.children)-1].children[0].tipo = p[1].valor #                                         \
        # -------------------------------------------------------------------------------------------------------------------
        no_atual = no_atual.children[0] # avança para próximo nó
        var_a_percorrer -= 1

def p_declaracao_variaveis_error (p):
    '''declaracao_variaveis : tipo DOISPONTOS error
                            | tipo DOISPONTOS'''
    print("Erro Sintático: erro na declaração de variáveis.")
    global tem_erro_yacc
    tem_erro_yacc = True
    global count
    count += 1
    no_erro = Node("erro/" + str(count))
    p[0] = Node("declaracao_variaveis/" + str(count), children=[p[1], no_erro])
    parser.errok()

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
        # --- cria o atributo "tipo" no nó de valor de "var", o qual será utilizado para guardar o tipo da variável
        noValor = Node(p[1]+"/"+str(count), valor=[p[1]], tipo=[""])
        p[0] = Node("var " + p[1] + "/" + str(count), children=[noValor])
    elif (len(p) == 3):
        noValor = Node(p[1]+"/"+str(count), valor=[p[1]], tipo=[""])
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
    '''indice : ECOLCHE error
              | error DCOLCHE
              | indice ECOLCHE error DCOLCHE
              | indice ECOLCHE error
              | indice error DCOLCHE
              | ECOLCHE error DCOLCHE
              | indice ECOLCHE DCOLCHE
    '''
    print("Erro Sintático: erro na indexação.")
    global tem_erro_yacc
    tem_erro_yacc = True
    global count
    count += 1
    no_erro = Node("erro/" + str(count))
    p[0] = Node("indice/" + str(count), children=[no_erro])
    parser.errok()

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
    nome_funcao = "" # Para preencher o escopo dos parâmetros

    #encontra no inicial p/ parametros
    if (len(p) == 3):
        no_atual = p[2].children[1]
        nome_funcao = p[2].children[0].valor[0]
    elif (len(p) == 2):
        no_atual = p[1].children[1]
        nome_funcao = p[1].children[0].valor[0]

    #parametros
    parametros = [["tipo"], ["nome"]]
    global tem_erro_yacc
    if (len(no_atual.leaves)>0 and (not tem_erro_yacc)):
        num_parametros = int(len(no_atual.leaves)/2)
    else:
        num_parametros = 0
    #acessa os tipos e nomes das variaveis
    for i in range(num_parametros):
        if (i < (num_parametros-1)):#se é o último parametro
            #tipo
            parametros[0].append( no_atual.children[1].children[0].valor[0] )
            #nome
            parametros[1].append( no_atual.children[1].children[1].valor[0] )
            tabela[no_atual.children[1].children[1].pos_var[0]] = nome_funcao # Preenche o escopo no parâmetro
        else:
            #tipo
            parametros[0].append( no_atual.children[0].children[0].valor[0] )
            #nome
            parametros[1].append( no_atual.children[0].children[1].valor[0] )
            tabela[no_atual.children[0].children[1].pos_var[0]] = nome_funcao # Preenche o escopo no parâmetro
        #tabela[no_atual.children[1].children[1].pos_var[0]] = nome_funcao
        #novo no
        no_atual = no_atual.children[0]

    if (len(p) == 3):
        p[0] = Node("declaracao_funcao/" + str(count), children=[p[1], p[2]])

        #guarda os parametros em 'escopo'
        new_line = ["FUNCAO", p[2].children[0].valor[0], p[1].valor[0], "", "", "", 1, 0, parametros, p.lineno(2), p.lexpos(2)]
        tabela.append(new_line)
    elif (len(p) == 2):
        p[0] = Node("declaracao_funcao/" + str(count), children=[p[1]])
        new_line = ["FUNCAO", p[2].children[0].valor[0], "void", "", "", "", 1, 0, parametros, p.lineno(1), p.lexpos(1)]
        tabela.append(new_line)

def p_cabecalho (p):
    '''cabecalho : ID EPAREN lista_parametros DPAREN corpo FIM
    '''
    global count
    count += 1
    noValor = Node("nome " + p[1] + " /" + str(count), valor=[p[1]])
    p[0] = Node("cabecalho/" + str(count), children=[noValor, p[3], p[5]])

    #insere escopo vas variaveis do corpo
    global variaveis
    for i in variaveis:
        tabela[i][5] = p[1]
    #limpa lista de variaveis
    variaveis = []

def p_lista_parametros (p):
    '''lista_parametros : lista_parametros VIRGULA parametro
												| parametro
												| vazio
    '''
    global count
    count += 1
    if (len(p) == 4):
        p[0] = Node("lista_parametros/" + str(count), children=[p[1], p[3]])
    elif (len(p) == 2):
        p[0] = Node("lista_parametros/" + str(count), children=[p[1]])
        #new_line = ["PARAMETRO", p[1].children[1].valor[0], p[1].children[0].valor[0], "", "", "funcao", "", p.lineno(1), p.lexpos(1)]
        #tabela.append(new_line)

def p_parametro (p):
    '''parametro : tipo DOISPONTOS ID
								 |  parametro ECOLCHE DCOLCHE
    '''
    global count
    count += 1
    if (p[2] == ":"):
        noValor = Node(p[3]+"/"+str(count), valor=[p[3]], pos_var=[len(tabela)]) # pos_var guarda a posição da variável-parâmetro na tabela para finalizar o seu preenchimento no cabeçalho da função
        p[0] = Node("parametro/" + str(count), children=[p[1], noValor])

        new_line = ["VARIAVEL", p[3], p[1].valor[0], "", "", "", 0, 0, "", p.lineno(2), p.lexpos(2)]
        tabela.append(new_line)
        variaveis.append( len(tabela)-1 )
    elif (p[2] == "["):
        p[0] = Node("parametro/" + str(count), children=[p[1]])

def p_parametro_error (p):
    '''parametro : tipo error ID
								 |  error ID
								 |  parametro error DCOLCHE
								 |  parametro ECOLCHE error
								 |  ID
								 |  tipo DOISPONTOS
								 |  tipo
								 |  DOISPONTOS ID
    '''
    print("Erro Sintático: erro na definição de parâmetros de função.")
    global tem_erro_yacc
    tem_erro_yacc = True
    global count
    count += 1
    no_erro = Node("erro/" + str(count))
    p[0] = Node("parametro/" + str(count), children=[no_erro])
    parser.errok()

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
    '''se : error expressao ENTAO corpo FIM
					| SE expressao error corpo FIM
					| error expressao ENTAO corpo SENAO corpo FIM
					| SE expressao error corpo SENAO corpo FIM
					| SE expressao ENTAO corpo error corpo FIM
					| SE expressao ENTAO corpo SENAO corpo
    '''
    print("Erro no bloco se.")

def p_repita (p):
    '''repita : REPITA corpo ATE expressao
    '''
    global count
    count += 1
    p[0] = Node("repita/" + str(count), children=[p[2], p[4]])

def p_repita_error (p):
    '''repita : error corpo ATE expressao
							| REPITA corpo error expressao
    '''

def p_atribuicao (p):
    '''atribuicao : var ATRIBUICAO expressao
    '''
    global count
    count += 1
    p[0] = Node("atribuicao/" + str(count), children=[p[1], p[3]])
    #new_line = ["ATRIBUICAO", p[1].children[0].valor[0], "", "", "", "", "", p.lineno(2), p.lexpos(2)]
    #tabela.append(new_line)

def p_leia (p):
    '''leia : LEIA EPAREN var DPAREN
    '''
    global count
    count += 1
    p[0] = Node("leia/" + str(count), children=[p[3]])

def p_leia_error (p):
    '''leia : LEIA EPAREN error DPAREN
    '''

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
    noValor = Node(p[1]+"/"+str(count), valor=[p[1]], tipo=["numero"])
    p[0] = Node("numero "+p[1]+" /"+str(count), children=[noValor])
		#p[0] = Node(str(p[1]))

def p_chamada_funcao (p):
    '''chamada_funcao : ID EPAREN lista_argumentos DPAREN
    '''
    global count
    count += 1
    p[0] = Node("chamada_funcao/" + str(count), children=[p[3]], valor=[p[1]])

    #argumentos
    argumentos = [["tipo"], ["nome"]]
    #print(p[3].leaves)
    #DotExporter(p[0]).to_picture("ap.png")

    if (len(p[3].leaves) == 1): # Trata o caso dos parâmetros serem 1, vazio ou muitos
        if ("expressao" in p[3].children[0].name):
            for i in p[3].leaves:
                print(i.tipo)
                argumentos[0].append( "" )
                argumentos[1].append( i.valor[0] )
        else:
            #print(p[3].children[0].name)
            pass
    else:
        for i in p[3].leaves:
            print(i.tipo)
            argumentos[0].append( "" )
            argumentos[1].append( i.valor[0] )

    new_line = ["CHAMADA", p[1], "", "", "", "", "", "", argumentos, p.lineno(2), p.lexpos(2)]
    tabela.append(new_line)

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
        #print("Erro Sintatico: '%s' na linha 4" %(p.value))
        print("Erro Sintatico: '%s' na linha '%d'" %(p.value, p.lineno))
        parser.errok()
    else:
        print("Erro!")

def p_vazio(p):
    '''vazio : '''
    #p[0] = Node("vazio")
    pass
    p[0] = Node("vazio/" + str(count), valor=["vazio"])




arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()

arvore = Node("inicial")
# Se o token for FUNCAO, posição 8 guarda o nome das variáveis e seus tipos
# Se o token for VARIAVEL ou FUNCAO, posição 6 guarda se ela foi lida/utilizada (1) ou não (0)
# Se o token for VARIAVEL, posição 6 recebe 1 se a variável foi inicializada e 0 caso contrário
# tabela = [["token", "lexema", "tipo", "dimensão", "tamanho", "escopo", "inicializado", "lin", "col"]]
"""
---------------------------------------------------------------------------------------------------------------
|                                                    TABELA                                                   |
---------------------------------------------------------------------------------------------------------------
|   0   |    1   |   2  |     3    |    4    |    5   |       6      |     7     |     8     |   9   |   10   |
---------------------------------------------------------------------------------------------------------------
| Token | Lexema | Tipo | Dimensão | Tamanho | Escopo | Inicializado | Utilizado | Variareis | Linha | Coluna |
---------------------------------------------------------------------------------------------------------------
==============
Explicação de cada campo:
- Token: guarda o valor do token que gerou a linha na tabela. Pode receber: VARIAVEL, FUNCAO, CHAMADA (para chamada de funções).
- Lexema: guarda o nome do elemento que gerou a linha na tabela. Se o token for FUNCAO, lexema guardará o nome da função. Se o token for VARIAVEL, lexema guardará o nome da variável.
- Tipo: se o token for FUNCAO, guarda o tipo do retorno da função. Se o token for VARIAVEL, guarda o tipo da variável.
- Dimensão: guarda a dimensão das variáveis. Por exemplo, vetores tem dimensão 1, matrizes tem dimensão 2.
- Tamanho: guarda o tamanho (quantidade de elementos) de cada dimensão da variável. Caso a variável tenha dimensão 0, o tamanho também será 0.
- Escopo: guarda o escopo de cada variável. Esse campo pode assumir o valor "global" ou, se a variável for local, assumirá o nome da função em que a variável foi declarada.
"""
tabela = [["token", "lexema", "tipo", "dimensão", "tamanho", "escopo", "inicializado", "utilizado", "variaveis", "lin", "col"]]
variaveis = [] # Guarda índice das variáveis já declaradas na tabela para definição do escopo

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
if not tem_erro_yacc:
    DotExporter(arvore).to_picture("grafo.png")


