from llvmlite import ir
from llvmlite import binding as llvm
import itertools

#from semantica_tzora import arvore, tabela, tem_erros
from semantica_tzora import arvore, tabela, getLinha


# ==========================
# === Funções Auxiliares ===
# ==========================
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
    declara_var_global()
    # Salva o Módulo
    arquivo = open('modulo.ll', 'w')
    arquivo.write(str(module))
    arquivo.close()
    print(module)


def declara_funcoes():
    for fn_symbol in self.context.symbols:
        if isinstance(fn_symbol, FunctionSymbol):

            parameters = []

            for var_symbol in self.context.symbols:
                if isinstance(var_symbol, VarSymbol) and var_symbol.scope == fn_symbol.name and var_symbol.parameter:
                    parameters.append(self.type_to_llvmlite_type(
                        var_symbol.type_, var_symbol.index_list))

            type_ = self.type_to_llvmlite_type(
                fn_symbol.type_, [])
            t_func = ir.FunctionType(type_, parameters)
            func = ir.Function(self.module, t_func, name=fn_symbol.name)

def declara_var_global():
    var_globais = retornaLista("VARIAVEL", "global")
    for var in var_globais:
        # Se var for flutuante
        tipo = ir.FloatType()
        val = 0.0
        # Se var for inteiro
        if (var[2] == "inteiro"):
            tipo = ir.IntType(32)
            val = 0

        print(var[1])
        # Variável inteira global g
        g = ir.GlobalVariable(module, tipo, var[1])
        # Inicializa a variavel g
        g.initializer = ir.Constant(tipo, val)
        # Linkage = common
        g.linkage = "common"
        # Define o alinhamento em 4 bytes
        g.align = 4

#if (tem_erros[0] != -1):
gera_codigo()
