from llvmlite import ir
from llvmlite import binding as llvm
import itertools

#from semantica_tzora import arvore, tabela, tem_erros
from semantica_tzora import arvore, tabela, getLinhaEspecifico


# ==========================
# === Variáveis Globais ===
# ==========================
"""
Dicionário que guarda a lista das variáveis
locais de cada função. Também inclui uma
lista para as variáveis globais.
{
    "global": [lista de variáveis globais],
    "<funcao>": [<lista de variáveis>]
}
"""
lista_variaveis = {"global": []}


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
Dado um nome de nó da árvore,
retorna apenas a string antes da barra.
"""
def retornaNomeFormatado(nome):
    return nome.split('/')[0]

"""
Devolve o elemento da folha (número ou variável)
no formato LLVM.
"""
def retornaValor(arvore, escopo):
    if (retornaNomeFormatado(arvore.name) == "numero"):
        # Cria uma constante pra armazenar o número
        if (arvore.children[0].tipo[0] == "inteiro"):
            return ir.Constant(ir.IntType(32).as_pointer(), int(arvore.children[0].valor[0]))
        elif (arvore.children[0].tipo[0] == "flutuante"):
            return ir.Constant(ir.FloatType().as_pointer(), float(arvore.children[0].valor[0]))
        
    elif (retornaNomeFormatado(arvore.name) == "var"):
        # --- Encontra variável ---
        # Guarda a variável que vai ser recebida
        # Nome da variável no nó
        nome_var_no = arvore.children[0].valor[0]
        for v in lista_variaveis[escopo]:
            if (v.name == retornaNomeFormatado(nome_var_no)):
                return v

    else:
        print("ERROR (código 89).")

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
    lista_variaveis[escopo] = []
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
    # *Cria o corpo da função func

    # Cria o bloco de entrada
    entryBlock = func.append_basic_block('entry')
    # Adiciona o bloco de entrada
    builder = ir.IRBuilder(entryBlock)

    # =========== Declara variáveis da função ===========
    var_locais = retornaLista("VARIAVEL", escopo)
    for var in var_locais:
        tipo = retornaTipoLlvm(var[2])

        # Cria variável local
        variavel = builder.alloca(tipo, name=var[1])
        # Define o alinhamento em 4 bytes
        variavel.align = 4

        # Adiciona na lista controladora de variáveis
        lista_variaveis[escopo].append(variavel)
    declara_var_local(escopo, builder)
    #print("vars: " + str(lista_variaveis))

    # =========== Percorre corpo da função ===========
    corpo = arvore.children[1].children[1]
    for i in range (1, len(corpo.children)-1):
        no_filho = corpo.children[i]

        # ----------- Percorre corpo da função -----------
        # ........... ATRIBUICAO ...........
        if (retornaNomeFormatado(no_filho.name) == "atribuicao"):
            print("164atrib")
            # Guarda a variável que vai receber a atribuição
            var_de_recebimento = None
            # Nome da variável no nó
            nome_var_no = no_filho.children[0].children[0].valor[0]
            # Encontra variável que vai receber a atribuição
            for v in lista_variaveis[escopo]:
                if (v.name == retornaNomeFormatado(nome_var_no)):
                    var_de_recebimento = v
                    break

            # --- Encontra elemento a ser recebido ---
            no_recebido = no_filho.children[1]
            if (retornaNomeFormatado(no_recebido.name) == "numero"):
                print("178numero")
                # Cria uma constante pra armazenar o número
                num = ir.Constant(ir.IntType(32), no_recebido.children[0].valor[0])
                # Armazena o número na variavel
                builder.store(num, var_de_recebimento)
                
            elif (retornaNomeFormatado(no_recebido.name) == "var"):
                print("178var")
                # --- Encontra variável a ser recebida ---
                # Guarda a variável que vai ser recebida
                var_recebida = None
                # Nome da variável no nó
                nome_var_no = no_recebido.children[0].valor[0]
                for v in lista_variaveis[escopo]:
                    if (v.name == retornaNomeFormatado(nome_var_no)):
                        var_recebida = v
                        break
                # Armazena var a ser recebida em temporário
                temp = builder.load(var_recebida,"")
                # Armazena valor na variável de recebimento
                builder.store(temp, var_de_recebimento)
            else:
                gera_operacao_matematica(no_recebido, builder, escopo)



            
    # =========== Cria bloco de saída da função ===========
    # Cria o bloco de saída
    endBasicBlock = func.append_basic_block('exit')
    # Cria um salto para o bloco de saída
    builder.branch(endBasicBlock)
    # Adiciona o bloco de saida
    builder.position_at_end(endBasicBlock)

    # return 0
    # Cria o return
    # returnVal_temp = builder.load(returnVal, name='', align=4)
    # builder.ret(returnVal_temp)
    builder.ret(ir.Constant(ir.IntType(32), 0))








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
        # Adiciona na lista controladora de variáveis
        lista_variaveis["global"].append(g)

def declara_var_local(funcao, builder):
    var_locais = retornaLista("VARIAVEL", "funcao")
    for var in var_locais:
        tipo = retornaTipoLlvm(var[2])

        # Aloca na memória a variável local
        l = builder.alloca(tipo, name=var[1])
        # Define o alinhamento
        l.align = 4

        lista_variaveis[funcao].append(l)

def gera_operacao_matematica(arvore, builder, escopo):
    oper1 = 0 # Operando da esquerda
    oper2 = 0 # Operando da direita

    #print("263leaf: " + str(arvore.children[0].children[0].is_leaf))
    # Determina valor do operando da esquerda
    if(not arvore.children[0].children[0].is_leaf):
        # Caso operando seja outra expressão matemática
        oper1 = gera_operacao_matematica(arvore.children[0], builder, escopo)
    else:
        oper1 = retornaValor(arvore.children[0], escopo)

    # Determina valor do operando da direita
    if(not arvore.children[1].children[0].is_leaf):
        # Caso operando seja outra expressão matemática
        oper2 = gera_operacao_matematica(arvore.children[1], builder, escopo)
    else:
        oper2 = retornaValor(arvore.children[1], escopo)

    #print("280 " + str(oper1.type() ))PointerType(int32)
    #print("280 " + str(type(ir.IntType(32).as_pointer()) ))
    #print("280 " + str(type(oper1) ))
    #print("280 " + str(oper1 is ir.IntType(32).as_pointer() ))
    #print("280 " + str(type(ir.PointerType(ir.IntType(32))) ))

    op = arvore.valor[0]
    tipo = "inteiro"

    # Converte operandos para o mesmo tipo
    if (not (type(oper1) == type(oper2)) ):
        oper1 = builder.sitofp(oper1, ir.FloatType().as_pointer())#IntType(32)
        oper2 = builder.sitofp(oper2, ir.FloatType().as_pointer())#FloatType()
        tipo= "flutuante"

    if (op == '+'):
        if tipo == "inteiro":
            return builder.add(oper1, oper2, "")

        return builder.fadd(oper1, oper2, "")

    elif (op == '-'):
        if tipo == "inteiro":
            return builder.sub(oper1, oper2, "")

        return builder.fsub(oper1, oper2, "")

    elif (op == '*'):
        if tipo == "inteiro":
            return builder.mul(oper1, oper2, "")

        return builder.fmul(oper1, oper2, "")

    elif (op == '/'):
        if tipo == "inteiro":
            return builder.sdiv(oper1, oper2, "")

        return builder.fdiv(oper1, oper2, "")


#if (tem_erros[0] != -1):
gera_codigo()
