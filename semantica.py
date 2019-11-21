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

# Retorna a linha de x
def getLinha(regra, pos, x, opcao=None):
	for i in range (len(tabela)):
		if (tabela[i][0] == regra):
			if (opcao == None and tabela[i][pos] == x):
				return i
			# Devolve posição de x em um escopo específico
			elif (opcao != None and tabela[i][pos] == x and (tabela[i][5] == opcao or tabela[i][5] == "global")):
				return i
	return -1



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
		var = no_atual.children[0].children[0].valor[0]
		if (not estaContido("VARIAVEL", 1, var, escopo)):
			global lista_mensagens
			mensagem = "ERRO: variável " + var + " está sendo usada, mas não foi declarada."
			lista_mensagens.append(mensagem)
			print(mensagem)
		else: # Registra que a variável foi inicializada
			pos = getLinha("VARIAVEL", 1, var, escopo)
			tabela[pos][6] = 1

		folhas = no_atual.children[1].leaves
		for j in folhas:
			pos = getLinha("VARIAVEL", 1, j.valor[0], escopo)
			if ( pos != -1):
				tabela[pos][9] = 1

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
	declaradas = []
	#print(tabela)

	# === Tem função principal ===
	if (not hasPrincipal()):
		mensagem = "ERRO: Programa não tem função principal."
		lista_mensagens.append(mensagem)
		print(mensagem)
		return -1

	# Percorre tabela de símbolos
	for i in range (len(tabela)):
		# === Olha quantidades de parâmetros ===
		# Encontra as funções
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

		# === Verifica se uma variável foi declarada mais de uma vez ===
		if (tabela[i][0] == "VARIAVEL"):
			if (((tabela[i][1]+tabela[i][5]) in declaradas) or ((tabela[i][1]+"global") in declaradas)):
				mensagem = "WARNING: Variável " + tabela[i][1] + " na linha " + str(tabela[i][7]) + " já foi declarada."
				lista_mensagens.append(mensagem)
				print(mensagem)
				#return -1
			declaradas.append(tabela[i][1]+tabela[i][5])

	# === Percorre Árvore ===
	percorreArvore(arvore)

	# === Verifica se as variáveis foram inicializadas ===
	for i in range (len(tabela)):
		if (tabela[i][0] == "VARIAVEL" and tabela[i][6] == 0):
			mensagem = "WARNING: Variável " + tabela[i][1] + " na linha " + str(tabela[i][7]) + " foi declarada mas não inicializada."
			lista_mensagens.append(mensagem)
			print(mensagem)
			return -1

	print(tabela)
MOSTRAR SE A VARIÁVEL NÃO FOI UTILIZADA
IGUAL A LINHA DE CIMA


varre_semantica()

