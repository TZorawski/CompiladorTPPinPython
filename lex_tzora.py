# ------------------------------------------------------------
# lex.py
# Analizador Lexico do compilador para a linguagem T++
#
# Autor: Thais Zorawski
# ------------------------------------------------------------
import sys
import ply.lex as lex

reserved = {
  'então' : 'ENTAO',
  'se' : 'SE',
  'fim': 'FIM',
  'senão': 'SENAO',
  'até': 'ATE',
  'inteiro': 'INTEIRO',
  'flutuante': 'FLUTUANTE',
  'repita': 'REPITA',
  'retorna': 'RETORNA',
  'leia': 'LEIA',
  'escreva': 'ESCREVA'
}

# List of token names.   This is always required
tokens = [
  'VIRGULA',
  'DOISPONTOS',
  'ATRIBUICAO',
  'ADICAO',
  'SUBTRACAO',
  'MULTIPLICACAO',
  'DIVISAO',
  'EPAREN',
  'DPAREN',
  'ECOLCHE',
  'DCOLCHE',
  'IGUAL',
  'DESIGUAL',
  'MAIORQ',
  'MENORQ',
  'MAIORIGUAL',
  'MENORIGUAL',
  'ELOGICO',
  'OULOGICO',
  'NEGACAO',
  'ID',
  'NUM_INTEIRO',
  'NUM_FLUTUANTE',
  'NUM_CIENTIFICO',
 ] + list(reserved.values())

# Regular expression rules for simple tokens
t_VIRGULA    = r','
t_DOISPONTOS    = r':'
t_ATRIBUICAO = r':='
t_ADICAO    = r'\+'
t_SUBTRACAO   = r'-'
t_MULTIPLICACAO   = r'\*'
t_DIVISAO  = r'/'
t_EPAREN  = r'\('
t_DPAREN  = r'\)'
t_ECOLCHE  = r'\['
t_DCOLCHE  = r'\]'
t_IGUAL = r'='
t_DESIGUAL = r'<>'
t_MAIORQ = r'>'
t_MENORQ = r'<'
t_MAIORIGUAL = r'>\='
t_MENORIGUAL = r'<\='
t_ELOGICO = r'\&\&'
t_OULOGICO = r'\|\|'
t_NEGACAO = r'\!'
t_NUM_INTEIRO = r'[+|-]?[0-9]+'
t_NUM_FLUTUANTE = r'[+|-]?[0-9]+\.[0-9]+'
t_NUM_CIENTIFICO = r'[+|-]?[0-9]+[\.[0-9]+]?[E|e][+|-]?[0-9]+'

# A regular expression rule with some action code
def t_ID(t):
     r'[a-z][\w_]*'
     t.type = reserved.get(t.value,'ID')    # Check for reserved words
     return t

def t_COMENTARIO(t):
     r'{[^}]*[^{]*}'
     # pass

# Define a rule so we can track line numbers
def t_newline(t):
    r'\n+'
    t.lexer.lineno += len(t.value)

# A string containing ignored characters (spaces and tabs)
t_ignore  = ' \t'

# Error handling rule
def t_error(t):
    print("Illegal character '%s'" % t.value[0])
    t.lexer.skip(1)

# Build the lexer
lexer = lex.lex()


# Parsing rules
precedence = (
    ('left','ADICAO','SUBTRACAO'),
    ('left','SUBTRACAO','MULTIPLICACAO'),
    ('left','MULTIPLICACAO','DIVISAO'),
    )

arq = open(sys.argv[1], 'r', encoding="utf8")
data = arq.read()

# Give the lexer some input
lexer.input(data)
 
# Tokenize
while True:
    tok = lexer.token()
    if not tok: 
        break      # No more input
    print(tok.type)