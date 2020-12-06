from llvmlite import ir
from llvmlite import binding as llvm
import itertools

#from semantica_tzora import arvore, tabela, tem_erros
from semantica_tzora import arvore, tabela, getLinhaEspecifico


# ==========================
# === Funções Auxiliares ===
# ==========================

"""
Retorna lista do elementos da tabela 
que são da regra dada. Se escopo for 
passado, retorna apenas elementos desse 
escopo.
"""
def retornaLista(regra, escopo=None):
    lista = []
    for item in tabela:
        #print(item)
        if (escopo == None):
            if (item[0] == regra):
                lista.append(item)
        else:
            if (item[0] == regra and item[5] == escopo):
                lista.append(item)
    return lista

"""
Dado um tipo (inteiro ou flutuante),
retorna o tipo do LLVM correspondente.
"""
def retornaTipoLlvm(tipo):
    tipo_basico = None
    if tipo == "inteiro":
        tipo_basico = ir.IntType(32)
    elif tipo == "flutuante":
        tipo_basico = ir.FloatType()
    else:
        tipo_basico = ir.VoidType()
        
    return tipo_basico

"""
Dado um tipo (inteiro ou flutuante),
retorna o tipo do LLVM correspondente.
"""
def retornaNomeFormatado(nome):
    return nome.split('/')[0]
# ==========================

llvm.initialize()
llvm.initialize_all_targets()
llvm.initialize_native_target()
llvm.initialize_native_asmprinter()


module = ir.Module('modulo.bc')
module.triple = llvm.get_default_triple()

target = llvm.Target.from_triple(module.triple)
target_machine = target.create_target_machine()

module.data_layout = target_machine.target_data


escrevaInteiro = ir.Function(module,ir.FunctionType(ir.VoidType(), [ir.IntType(32)]),name="escrevaInteiro")
escrevaFlutuante = ir.Function(module,ir.FunctionType(ir.VoidType(),[ir.FloatType()]),name="escrevaFlutuante")
leiaInteiro = ir.Function(module,ir.FunctionType(ir.IntType(32),[]),name="leiaInteiro")
leiaFlutuante = ir.Function(module,ir.FunctionType(ir.FloatType(),[]),name="leiaFlutuante")


def gera_codigo():
    #print(tabela)
    declara_var_global() # Declara as variáveis globais

    percorre_arvore(arvore) # Percorre a árvore
    
    # Salva o Módulo
    arquivo = open('modulo.ll', 'w')
    arquivo.write(str(module))
    arquivo.close()
    print(module)


def percorre_arvore(arvore):
    regra = retornaNomeFormatado(arvore.name)
    if (regra == "declaracao_funcao"):
        declara_funcoes(arvore)

    for child in arvore.children:
        percorre_arvore(child)

def declara_funcoes(arvore):
    escopo = arvore.children[1].valor[0] # Nome da função
    pos = getLinhaEspecifico("FUNCAO", 1, escopo)
    print("92foncao " + escopo)

    # =========== Cria o cabeçalho da função ===========
    # Pega os tipos dos parametros
    tipos_parametros = []
    for i in range (1, len(tabela[pos][8][0])):
        tipo_par = retornaTipoLlvm(tabela[pos][8][0][i])
        tipos_parametros.append(tipo_par)

    print("101par t:" + str(tipos_parametros))
    # Declara a função
    tipo_funcao = retornaTipoLlvm(tabela[pos][2])
    t_func = ir.FunctionType(tipo_funcao, tipos_parametros)
    func = ir.Function(module, t_func, name=escopo)

    # Declara parametros
    for i in range (1, len(tabela[pos][8][1])):
        par = tabela[pos][8][1][i]
        print("110par :" + par)
        func.args[i-1].name = par

    # =========== Cria bloco de entrada da função ===========
    # Cria o corpo da função func
    entryBlock = func.append_basic_block('entry')
    builder = ir.IRBuilder(entryBlock)

    # =========== Declara variáveis da função ===========
    var_locais = retornaLista("VARIAVEL", escopo)
    for var in var_locais:
        tipo = retornaTipoLlvm(var[2])

        # Cria variável local
        variavel = builder.alloca(tipo, name=var[1])
        #builder.store(ir.Constant(ir.IntType(32), 0), variavel)
        # Define o alinhamento em 4 bytes
        variavel.align = 4

    # =========== Percorre corpo da função ===========
    corpo = arvore.children[1].children[1]










def declara_var_global():
    var_globais = retornaLista("VARIAVEL", "global")
    for var in var_globais:
        tipo = retornaTipoLlvm(var[2])
        #tipo = ir.FloatType()
        val = 0.0 # Se var for flutuante
        if (var[2] == "inteiro"):
            #tipo = ir.IntType(32)
            val = 0 # Se var for inteiro

        # Cria variável global
        g = ir.GlobalVariable(module, tipo, var[1])
        # Inicializa a variavel
        g.initializer = ir.Constant(tipo, val)
        # Linkage = common
        g.linkage = "common"
        # Define o alinhamento em 4 bytes
        g.align = 4

def declara_var_local(funcao):
    var_locais = retornaLista("VARIAVEL", "funcao")
    for var in var_locais:
        tipo = retornaTipoLlvm(var[2])

        print(var[1])

        # Aloca na memória a variável local
        l = builder.alloca(tipo, name=var[1])
        # Define o alinhamento
        l.align = 4

#if (tem_erros[0] != -1):
gera_codigo()
