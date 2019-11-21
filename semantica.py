from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from yacc_tzora import arvore, tabela

# =========================
# === Variáveis Globais ===
# =========================
# Guarda mensagens da varredura
lista_mensagens = []
# Guarda escopo percorrido no momento
escopo = "global"


# Retorna se x exite em alguma regra dada
def estaContido(regra, pos, x, opcao=None):
	for i in tabela:
		if (i[0] == regra):
			if (opcao == None and i[pos] == x):
				return True
			# Verifica a regra em um escopo específico
			elif (opcao != None and i[pos] == x and (i[5] == opcao or i[5] == "global")):
				return True
	return False



# Verifica se a função Principal existe
def hasPrincipal():
	has = False
	for i in tabela:
		if ("principal" in i):
			has = True
	return has



# Percorre árvore em profundidade
def percorreArvore(no_atual):
	#print(no_atual.name)
	global escopo
	# ------------------
	# --- Trata o nó ---
	# ------------------

	# Define escopo (ao entrar na função)
	if ("declaracao_funcao/" in no_atual.name):
		escopo = no_atual.children[1].children[0].valor[0]

	# Trata atribuições
	if ("atribuicao/" in no_atual.name):
		#global escopo
		var = no_atual.children[0].children[0].valor[0]
		print("escopo " + escopo)
		if (not estaContido("VARIAVEL", 1, var, escopo)):
			global lista_mensagens
			mensagem = "ERRO: variável " + var + " está sendo usada, mas não foi declarada."
			lista_mensagens.append(mensagem)
			print(mensagem)

	# Percorre filhos
	for i in no_atual.children:
		percorreArvore(i)

	# Defina escopo (ao sair da função)
	if ("declaracao_funcao/" in no_atual.name):
		#global escopo
		escopo = "global"



# Faz varredura semântica
def varre_semantica():
	global lista_mensagens
	#print(tabela)

	# === Tem função principal ===
	if (not hasPrincipal()):
		mensagem = "ERRO: Programa não tem função principal."
		lista_mensagens.append(mensagem)
		print(mensagem)
		return -1

	# === Olha quantidades de parâmetros ===
	# Encontra as funções
	for i in range (len(tabela)):
		if (tabela[i][0] == "FUNCAO"):

			# Encontra as chamadas funções
			for j in range (len(tabela)):
				if (tabela[j][0] == "CHAMADA" and tabela[j][1] == tabela[i][1]):
					# Compara se o num de parametros é o mesmo
					if (len(tabela[i][5][1]) != len(tabela[j][5][1])):
								mensagem = "ERRO: A função " + tabela[i][1] + " deve ter " + str(len(tabela[i][5][1]) - 1) + " parâmetros e ela foi chamada com " + str(len(tabela[j][5][1]) - 1) + " parâmetros."
								lista_mensagens.append(mensagem)
								print(mensagem)
								return -1
	CONTAR QUANTAS VEZES UMA VARIÁVEL É USADA
	DAR WARNING QUANDO UMA VARIÁVEL FOR DECLARADA MAIS DE UMA VEZ

	# === Percorre Árvore ===
	percorreArvore(arvore)



varre_semantica()

