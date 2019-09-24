 # Yacc example
 """
 ARRUMAR OPERAÇÕES DENTRO DOS IFS
 """
 import ply.yacc as yacc
 
 # Get the token map from the lexer.  This is required.
 from lex_tzora import tokens


def programa (p):
    'programa : lista_declaracoes'
    p[0] = p[1]

def lista_declaracoes (p):
    '''lista_declaracoes : lista_declaracoes declaracao
                         | declaracao '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = p [1] p[2]

def declaracao (p):
    '''declaracao : declaracao_variaveis
                  | inicializacao_variaveis
                  | declaracao_funcao
    '''
    p[0] = p[1]

def declaracao_variaveis (p):
    'declaracao_variaveis : tipo DOISPONTOS lista_variaveis'
    p[0] = p[1] : p[3]

def inicializacao_variaveis (p):
    'inicializacao_variaveis : atribuicao'
    p[0] = p[1]

def lista_variaveis (p):
    '''lista_variaveis : lista_variaveis "," var 
                       | var
    '''
    if (len(p) == 4):
        p[0] = p[1] , p[3]
    elif (len(p) == 2):
        p[0] = p[1]

def var (p):
    '''var : ID
           | ID indice
    '''
    if (len(p) == 2):
        p[0] = p[1]
    elif (len(p) == 3):
        p[0] = p[1] p[2]

def indice (p):
    '''indice : indice ECOLCHE expressao DCOLCHE
              | ECOLCHE expressao DCOLCHE
    '''
    if (len(p) == 5):
        p[0] = p[1] [ p[3] ]
    elif (len(p) == 4):
        p[0] = p [1] p [2]




 
 def p_expression_plus(p):
     'expression : expression PLUS term'
     p[0] = p[1] + p[3]
 
 def p_expression_minus(p):
     'expression : expression MINUS term'
     p[0] = p[1] - p[3]
 
 def p_expression_term(p):
     'expression : term'
     p[0] = p[1]
 
 def p_term_times(p):
     'term : term TIMES factor'
     p[0] = p[1] * p[3]
 
 def p_term_div(p):
     'term : term DIVIDE factor'
     p[0] = p[1] / p[3]
 
 def p_term_factor(p):
     'term : factor'
     p[0] = p[1]
 
 def p_factor_num(p):
     'factor : NUMBER'
     p[0] = p[1]
 
 def p_factor_expr(p):
     'factor : LPAREN expression RPAREN'
     p[0] = p[2]
 
 # Error rule for syntax errors
 def p_error(p):
     print("Syntax error in input!")
 
 # Build the parser
 parser = yacc.yacc()
 
 while True:
    try:
        s = raw_input('calc > ')
    except EOFError:
        break
    if not s: continue
    result = parser.parse(s)
    print(result)