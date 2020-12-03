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
    #if (lista == ['corpo', 'lista_parametros', 'lista_argumentos', 'lista_variaveis']):
    #    print(x)
    for item in lista:
        if (x == item):
            #if (lista == ['corpo', 'lista_parametros', 'lista_argumentos', 'lista_variaveis']):
            #    print(x + '=' + item)
            esta = True
            break
    return esta

# ----- Poda -----

def poda_arvore(arvore):
    #print("nome: " + arvore.name)
    for no in arvore.children:
        poda_arvore(no)

    if(estaNaLista(arvore.name, OPERATIONS)):
        #print("prune_especial")
        prune_especial(arvore)

    if(estaNaLista(arvore.name, NOS_SIMPLES)):
        #print("prune_one_node no simples")
        prune_one_node(arvore)

    if(estaNaLista(arvore.name, ['corpo']) and len(arvore.children) == 0):
        #print("prune_one_node apaga")
        erased_node(arvore)
        
    elif(estaNaLista(arvore.name, ['corpo', 'lista_parametros', 'lista_argumentos', 'lista_variaveis'])):
        #print('ppai' + arvore.parent.name.split('/')[0] + ':' + arvore.name.split('/')[0])
        if(arvore.parent.name.split('/')[0] == arvore.name.split('/')[0]):
            print("nome: " + arvore.name)
            print("prune_one_node lista")
            prune_one_node(arvore)

# ----- Prunning Functions -----
def prune_especial(tree):
    aux = []

    if(estaNaLista(tree.parent.name, ["operador_soma", "operador_multiplicacao"])):
        prune_one_node(tree.parent)

    dad = tree.parent
    aux = [dad.children[0], dad.children[2]] 
    tree.children = aux
    dad.children = [tree]
    
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
    
