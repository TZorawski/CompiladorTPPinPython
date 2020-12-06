"""
Poda a árvore.
Autor: Thais Zorawski
Data: 02/12/2020
"""

# ----- Constantes -----
OPERATIONS = ['+', '-', '*', '/', ':=', ':']
NOS_SIMPLES = [
    'acao', 'expressao', 'expressao_logica', 'expressao_simples', 'expressao_aditiva', 
    'expressao_multiplicativa', 'expressao_unaria', 'operador_relacional', 
    'operador_logico', 'operador_negacao', 'fator', 'lista_declaracoes',
    'declaracao'
    ]

# ----- Funções Auxiliares -----
def estaNaLista(x, lista):
    # Retorna True se a string "x" está presente em algum item da lista de strings "lista"
    esta = False
    x = x.split('/')[0]
    for item in lista:
        if (x == item):
            esta = True
            break
    return esta

# ----- Poda -----

def poda_arvore(arvore):
    for no in arvore.children:
        poda_arvore(no)

    if(estaNaLista(arvore.name, OPERATIONS)):
        #print("poda_operadores")
        poda_operadores(arvore)

    if(estaNaLista(arvore.name, NOS_SIMPLES)):
        #print("prune_one_node no simples")
        prune_one_node(arvore)

    if(estaNaLista(arvore.name, ['corpo']) and len(arvore.children) == 0):
        #print("prune_one_node apaga")
        erased_node(arvore)
        
    elif(estaNaLista(arvore.name, ['corpo', 'lista_parametros', 'lista_argumentos', 'lista_variaveis'])):
        if(arvore.parent.name.split('/')[0] == arvore.name.split('/')[0]):
            #print("prune_one_node lista")
            prune_one_node(arvore)

    if(estaNaLista(arvore.name, ['cabecalho'])):
        poda_cabecalho_func(arvore)

# ----- Prunning Functions -----
# Poda nó de operadores
def poda_operadores(arvore):
    aux = []

    if(estaNaLista(arvore.parent.name, ["operador_soma", "operador_multiplicacao"])):
        prune_one_node(arvore.parent)

    dad = arvore.parent
    aux = [dad.children[0], dad.children[2]] 
    arvore.children = aux
    dad.children = [arvore]

# Poda nó de cabeçalho de funções
def poda_cabecalho_func(arvore):
    aux = []

    dad = arvore.parent
    filhos_nome = [arvore.children[1], arvore.children[2]]
    no_nome = arvore.children[0]
    no_nome.children = filhos_nome # Nó de nome da função vira pai
    filhos_dad = [dad.children[0], no_nome] 
    dad.children = filhos_dad
    
def prune_one_node(tree):
    aux = []
    dad = tree.parent

    for i in range(len(dad.children)):
        if (dad.children[i].name == tree.name):
            aux += tree.children
        else:
            aux.append(dad.children[i])

    dad.children = aux

def erased_node(tree):
    aux = []
    dad = tree.parent

    for i in range(len(dad.children)):
        if (not (dad.children[i].name == tree.name)):
            aux.append(dad.children[i])

    dad.children = aux
    
