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
locais de cada função e seus tipos. Também inclui uma
lista para as variáveis globais e seus tipos. O tipo
pode ser "inteiro" ou "flutuante".
{
    "global": [ [<variável global>, <tipo da variável global>] ],
    "<funcao>": [ [<variável local>, <tipo da variável local>] ]
}
"""
lista_variaveis = {"global": []}

"""
Dicionário que guarda a lista das funções e seus tipos de retorno.
O tipo pode ser "inteiro" ou "flutuante".
{
    "<nome_funcao>": [ [<função>, <tipo da funcao>] ]
}
"""
lista_funcoes = {}

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
        if (arvore.children[0].tipo[0] == "inteiro" or (arvore.children[0].valor[0].isdigit()) ):
            return ir.Constant(ir.IntType(32).as_pointer(), int(arvore.children[0].valor[0]))
        elif (arvore.children[0].tipo[0] == "flutuante"):
            return ir.Constant(ir.FloatType().as_pointer(), float(arvore.children[0].valor[0]))
        else:
            return ir.Constant(ir.FloatType().as_pointer(), float(arvore.children[0].valor[0]))
        
    elif (retornaNomeFormatado(arvore.name) == "var"):
        # --- Encontra variável ---
        # Guarda a variável que vai ser recebida
        # Nome da variável no nó
        nome_var_no = arvore.children[0].valor[0]
        for v in (lista_variaveis[escopo] + lista_variaveis["global"]):
            if (v[0].name == retornaNomeFormatado(nome_var_no)):
                return v

    else:
        print("ERROR (código 89).")

"""
Devolve o elemento da folha (número ou variável)
no formato LLVM e o seu tipo (inteiro ou flutuante).
"""
def retornaValorTipo(arvore, escopo):
    if (retornaNomeFormatado(arvore.name) == "numero"):
        # Cria uma constante pra armazenar o número
        if (arvore.children[0].tipo[0] == "inteiro" or (arvore.children[0].valor[0].isdigit()) ):
            return [ir.Constant(ir.IntType(32).as_pointer(), int(arvore.children[0].valor[0])), "inteiro"]
        elif (arvore.children[0].tipo[0] == "flutuante"):
            return [ir.Constant(ir.FloatType().as_pointer(), float(arvore.children[0].valor[0])), "flutuante"]
        else:
            return [ir.Constant(ir.FloatType().as_pointer(), float(arvore.children[0].valor[0])), "flutuante"]
        
    elif (retornaNomeFormatado(arvore.name) == "var"):
        # --- Encontra variável ---
        # Guarda a variável que vai ser recebida
        # Nome da variável no nó
        nome_var_no = arvore.children[0].valor[0]
        for v in (lista_variaveis[escopo] + lista_variaveis["global"]):
            if (v[0].name == retornaNomeFormatado(nome_var_no)):
                return v

    else:
        print("ERROR (código 89).")


# ==========================
# === Geraçao do Código ===
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
    print("\nCódigo:\n")
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
    lista_funcoes[escopo] = [func, tabela[pos][2]]

    # =========== Cria bloco de entrada da função ===========
    # *Cria o corpo da função func

    # Cria o bloco de entrada
    entryBlock = func.append_basic_block('entry')
    # Adiciona o bloco de entrada
    builder = ir.IRBuilder(entryBlock)

    # --- Cria o valor de retorno e inicializa com zero ---
    # Declarando e alocando a variável de retorno com o tipo inteiro
    retorno = builder.alloca(ir.IntType(32).as_pointer(), name='retorno')
    # Define uma constande 0 do tipo i32
    Zero32 = ir.Constant(ir.IntType(32).as_pointer(), 0) 
    # Armazena o 0 na váriavel de retorno
    builder.store(Zero32, retorno)

    # =========== Declara variáveis da função ===========
    # Recebe as linhas da tabela de regra "VARIAVEL" com o escopo dessa função
    var_locais = retornaLista("VARIAVEL", escopo)
    for var in var_locais:
        tipo = retornaTipoLlvm(var[2])

        # Cria variável local
        variavel = builder.alloca(tipo, name=var[1])
        # Define o alinhamento em 4 bytes
        variavel.align = 4

        # Adiciona na lista controladora de variáveis
        lista_variaveis[escopo].append([variavel, var[2]])
    #declara_var_local(escopo, builder)
    #print("vars: " + str(lista_variaveis))

    # =========== Percorre corpo da função ===========
    corpo = arvore.children[1].children[1]
    for i in range (1, len(corpo.children)):
        no_filho = corpo.children[i]

        # ----------- Percorre corpo da função -----------
        # ........... ATRIBUICAO ...........
        if (retornaNomeFormatado(no_filho.name) == "atribuicao"):
            print("164atrib")
            # Guarda a variável que vai receber a atribuição
            var_de_recebimento = None
            tipo_var_de_recebimento = "inteiro"
            tipo_var_recebido = "inteiro"
            # Nome da variável no nó
            nome_var_no = no_filho.children[0].children[0].valor[0]
            # Encontra variável que vai receber a atribuição
            for v in (lista_variaveis[escopo] + lista_variaveis["global"]):
                if (v[0].name == retornaNomeFormatado(nome_var_no)):
                    var_de_recebimento = v[0]
                    tipo_var_de_recebimento = v[1]
                    break

            # --- Encontra elemento a ser recebido ---
            no_recebido = no_filho.children[1]
            if (retornaNomeFormatado(no_recebido.name) == "chamada_funcao"):
                var_retorno = solve_func_call(no_recebido, builder, escopo)
                builder.store(var_retorno, var_de_recebimento)
                
            elif (retornaNomeFormatado(no_recebido.name) == "numero"):
                print("210numero")
                # Cria uma constante pra armazenar o número
                num = None
                if (no_recebido.children[0].tipo[0] == "inteiro"):
                    num = ir.Constant(ir.IntType(32), int(no_recebido.children[0].valor[0]))
                    tipo_var_recebido = "inteiro"
                elif (no_recebido.children[0].tipo[0] == "flutuante"):
                    num = ir.Constant(ir.FloatType(), float(no_recebido.children[0].valor[0]))
                    tipo_var_recebido = "flutuante"
                
                # Armazena o número na variavel
                builder.store(num, var_de_recebimento)
                
            elif (retornaNomeFormatado(no_recebido.name) == "var"):
                print("210var")
                # --- Encontra variável a ser recebida ---
                # Guarda a variável que vai ser recebida
                var_recebida = None
                # Nome da variável no nó
                nome_var_no = no_recebido.children[0].valor[0]
                for v in (lista_variaveis[escopo] + lista_variaveis["global"]):
                    if (v[0].name == retornaNomeFormatado(nome_var_no)):
                        var_recebida = v[0]
                        tipo_var_recebido = v[1]
                        break
                # Armazena var a ser recebida em temporário
                temp = builder.load(var_recebida,"")
                # Armazena valor na variável de recebimento
                builder.store(temp, var_de_recebimento)
            else:
                
                # Armazena valor a ser recebido em temporário
                aux = gera_operacao_matematica(no_recebido, builder, escopo)
                tipo_var_recebido = aux[1]
                temp = None
                if (aux[1] == "inteiro" and tipo_var_de_recebimento == "flutuante"):
                    aux[0] = builder.sitofp(aux[0], ir.FloatType())
                elif (aux[1] == "flutuante" and tipo_var_de_recebimento == "inteiro"):
                    aux[0] = builder.fptosi(aux[0], ir.IntType(32))

                # Armazena var a ser recebida em temporário
                temp = builder.load(aux[0],"")
                # Armazena valor na variável de recebimento
                builder.store(temp, var_de_recebimento)
                
                # Armazena valor na variável de recebimento
                #builder.store(temp, var_de_recebimento)
                #ero32 = ir.Constant(ir.IntType(32), 0) 
                #builder.store(ero32, var_de_recebimento)

        # ........... RETORNA ...........
        if ( i == (len(corpo.children) - 1) ):
            # =========== Cria bloco de saída da função ===========
            # Cria o bloco de saída
            endBasicBlock = func.append_basic_block('exit')
            # Cria um salto para o bloco de saída
            builder.branch(endBasicBlock)
            # Adiciona o bloco de saida
            builder.position_at_end(endBasicBlock)
            
            # Se há instrução de retorno
            if (retornaNomeFormatado(no_filho.name) == "retorna"):
                # Armazena valor de retorno
                valor = retornaValorTipo(no_filho.children[0], escopo)
                builder.store(valor[0], retorno)
                
            #builder.ptrtoint(retorno, ir.IntType(32))
            # Cria o return
            returno_temp = builder.load(retorno, name='ret_temp', align=4)
            builder.ret(returno_temp)
            
    

    








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
        lista_variaveis["global"].append([g, var[2]])

def declara_var_local(escopo, builder):
    var_locais = retornaLista("VARIAVEL", escopo)
    for var in var_locais:
        tipo = retornaTipoLlvm(var[2])

        # Aloca na memória a variável local
        l = builder.alloca(tipo, name=var[1])
        # Define o alinhamento
        l.align = 4

        lista_variaveis[funcao].append([l, var[2]])

def gera_operacao_matematica(arvore, builder, escopo):
    oper1 = 0 # Operando da esquerda
    tipo_oper1 = "inteiro"
    c = 0 # Operando da direita
    tipo_oper2 = "inteiro"
    tipo = "inteiro" # Tipo da operação

    #print("263leaf: " + str(arvore.children[0].children[0].is_leaf))
    # Determina valor do operando da esquerda
    if(not arvore.children[0].children[0].is_leaf):
        # Caso operando seja outra expressão matemática
        aux = gera_operacao_matematica(arvore.children[0], builder, escopo)
        oper1 = aux[0]
        tipo_oper1 = aux[1]
    else:
        aux = retornaValorTipo(arvore.children[0], escopo)
        oper1 = aux[0]
        tipo_oper1 = aux[1]

    # Determina valor do operando da direita
    if(not arvore.children[1].children[0].is_leaf):
        # Caso operando seja outra expressão matemática
        aux = gera_operacao_matematica(arvore.children[1], builder, escopo)
        oper2 = aux[0]
        tipo_oper2 = aux[1]
    else:
        aux = retornaValorTipo(arvore.children[1], escopo)
        oper2 = aux[0]
        tipo_oper2 = aux[1]

    op = arvore.valor[0]

    # Converte operandos para o mesmo tipo
    if (tipo_oper1 == "inteiro"  and tipo_oper2 == "flutuante"):
        oper1 = builder.sitofp(oper1, ir.FloatType().as_pointer())
        tipo= "flutuante"
    elif (tipo_oper1 == "flutuante"  and tipo_oper2 == "inteiro"):
        oper2 = builder.sitofp(oper2, ir.FloatType().as_pointer())
        tipo= "flutuante"
    else: # Se operandos tem mesmo tipo
        tipo = tipo_oper1

    if (op == '+'):
        if tipo == "inteiro":
            return [builder.add(oper1, oper2, ""), "inteiro"]

        return [builder.fadd(oper1, oper2, ""), "flutuante"]

    elif (op == '-'):
        if tipo == "inteiro":
            return [builder.sub(oper1, oper2, ""), "inteiro"]

        return [builder.fsub(oper1, oper2, ""), "flutuante"]

    elif (op == '*'):
        if tipo == "inteiro":
            return [builder.mul(oper1, oper2, ""), "inteiro"]

        return [builder.fmul(oper1, oper2, ""), "flutuante"]

    elif (op == '/'):
        if tipo == "inteiro":
            return [builder.sdiv(oper1, oper2, ""), "inteiro"]

        return [builder.fdiv(oper1, oper2, ""), "flutuante"]

def solve_func_call(arvore, builder, escopo):
    params = []

    funcao_chamada = tabela[getLinhaEspecifico("FUNCAO", 1, arvore.valor[0])]
    func, tipo_func = lista_funcoes[funcao_chamada[1]]
    if(len(arvore.children[0].children) > 0):
        for no_par in arvore.children[0].children:
            if(retornaNomeFormatado(no_par.name) == "var"):
                par = retornaValor(no_par, escopo)
                params.append(
                    builder.load(par[0])
                )
            elif(retornaNomeFormatado(no_par.name) == "numero"):
                par = retornaValor(no_par, escopo)
                params.append(
                    par[0]
                )
        return builder.call(func, params)

    else:
        return builder.call(func, [])


#if (tem_erros[0] != -1):
gera_codigo()
