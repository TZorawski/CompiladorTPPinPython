from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from yacc_tzora import arvore, tabela, tem_erro_yacc
import poda_arvore_tzora as poda

"""
tratar tipo indice vetor e intervalo
tratar tipo coersao atribuição
tratar função duplicada
arrumar atribuição por leia
"""


# =========================
# === Variáveis Globais ===
# =========================
# Guarda mensagens da varredura
lista_mensagens = []
# Guarda escopo percorrido no momento
escopo = "global"


# ==========================
# === Funções Auxiliares ===
# ==========================
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

# Retorna a linha de x, sem considerar a opção "global" para o escopo
def getLinhaEspecifico(regra, pos, x, opcao=None):
	for i in range (len(tabela)):
		if (tabela[i][0] == regra):
			if (opcao == None and tabela[i][pos] == x):
				return i
			# Devolve posição de x em um escopo específico
			elif (opcao != None and tabela[i][pos] == x and (tabela[i][5] == opcao)):
				return i
	return -1


# Retorna se x é parâmetro da função "escopo"
def serParametroDaFuncao(escopo, x):
	pos = getLinhaEspecifico("FUNCAO", 1, escopo)
	lista_var = tabela[pos][8][1]
	for i in range (1,len(lista_var)):
		if (x == lista_var[i]):
			return True
	return False


# Verifica se a função Principal existe
def hasPrincipal():
	has = False
	for i in tabela:
		if ("principal" in i):
			has = True
	return has


# ====================================
# === Funções de Análise Semantica ===
# ====================================
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

	# Trata retorno da função
	if ("retorna/" in no_atual.name):
		if (not (no_atual.leaves[0].tipo[0] == "numero")):
			var_retorno = no_atual.leaves[0].valor[0]
			pos_var_retorno = getLinhaEspecifico("VARIAVEL", 1, var_retorno, opcao=escopo)
			tabela[pos_var_retorno][7] = 1 # Declara que a variável foi utilizada
			if (  (pos_var_retorno == -1)  and  (not serParametroDaFuncao(escopo, var_retorno))  ):
				mensagem = "ERROR: variável " + var_retorno + " está sendo usada, mas não foi declarada em " + escopo + "."
				lista_mensagens.append(mensagem)
				print(mensagem)
				return -1
			else:
				pos_escopo = getLinha("FUNCAO", 1, escopo)
				if (tabela[pos_var_retorno][2] != tabela[pos_escopo][2]):
					mensagem = "ERROR: variável  de retorno da função " + escopo + " é do tipo " + tabela[pos_var_retorno][2] + ", mas o tipo esperado é " + tabela[pos_escopo][2] + "."
					lista_mensagens.append(mensagem)
					print(mensagem)
					return -1
	
	# Trata chamada função
	if ("chamada_funcao/" in no_atual.name):
		nome_func = no_atual.valor[0] #Nome função chamada
		# Encontra a definição da função chamada
		pos_definicao = getLinha("FUNCAO", 1, nome_func)
		pos_escopo = getLinha("FUNCAO", 1, escopo)

		if ( pos_definicao == -1):
			mensagem = "ERROR: função " + nome_func + " chamada na função " + escopo + " não existe."
			lista_mensagens.append(mensagem)
			print(mensagem)
			return -1
		elif ( (escopo == "principal") and (nome_func == "principal") ):
			mensagem = "WARNING: chamada recursiva para a função principal."
			lista_mensagens.append(mensagem)
			print(mensagem)
		elif (nome_func == "principal"):
			mensagem = "ERROR: chamada para a função principal não permitida."
			lista_mensagens.append(mensagem)
			print(mensagem)
			return -1

		# === Olha o tipo dos parâmetros das funções ===
		# Encontra as chamadas funções
		esta_correto = False # Auxiliar para verificar se existe chamada compatível com os tipo da declaração da função
		for j in range (1, len(tabela)):
			# tabela[pos_definicao] é a declaração da função, tabela[j] é a chamada da função
			if (tabela[j][0] == "CHAMADA" and tabela[j][1] == tabela[pos_definicao][1]):

				# ... Preenche tipo dos parâmetros das chamadas de função ...
				# ... * Passo necessário, pois na sintática não preenche tipo de parâmetros ...
				if ( (len(tabela[j][8][1]) > 1) and tabela[j][8][0][1] == ""): # Testa se os tipos estão vazios
					for k in range (len(tabela[j][8][1])-1):
						existe_escopo_local = getLinhaEspecifico("VARIAVEL", 1, tabela[j][8][1][k+1], opcao=tabela[pos_escopo][1]) # Testa se cada variável da chamada foi criada localmente
						if (existe_escopo_local != -1):
							tabela[j][8][0][k+1] = tabela[existe_escopo_local][2] # Atribui o tipo para o parâmetro
							tabela[existe_escopo_local][7] = 1 # Declara que a variável foi utilizada
						else:
							existe_escopo_global = getLinhaEspecifico("VARIAVEL", 1, tabela[j][8][1][k+1], opcao="global") # Testa se cada variável da chamada foi criada globalmente
							if (existe_escopo_global != -1):
								tabela[j][8][0][i+1] = tabela[existe_escopo_global][2] # Atribui o tipo para o parâmetro
								tabela[existe_escopo_global][7] = 1 # Declara que a variável foi utilizada
							else:
								mensagem = "ERROR: Variável " + tabela[j][8][1][k+1] + " passada como parâmetro da função " + tabela[j][1] + " chamada na função " + escopo + " não foi declarada."
								lista_mensagens.append(mensagem)
								print(mensagem)
								return -1

				# ... Preenchidos os tipo, verifica se estão corretos ...
				for k in range (len(tabela[j][8][0])-1):
					if (tabela[j][8][0][k+1] != tabela[pos_definicao][8][0][k+1]) :
						mensagem = "WARNING: Variável " + tabela[j][8][1][k+1] + " passada como parâmetro da função " + tabela[j][1] + " chamada na função " + escopo + " é do tipo " + tabela[j][8][0][k+1] + " e o tipo esperado é " + tabela[pos_definicao][8][0][k+1] + "."
						lista_mensagens.append(mensagem)
						print(mensagem)

	# Trata atribuições
	if ("atribuicao/" in no_atual.name):
		var = no_atual.children[0].children[0].valor[0]
		if ( (not estaContido("VARIAVEL", 1, var, escopo)) and (not serParametroDaFuncao(escopo, var))):
			mensagem = "ERROR: variável " + var + " está sendo usada, mas não foi declarada em " + escopo + "."
			lista_mensagens.append(mensagem)
			print(mensagem)
			return -1
		else: # Registra que a variável foi inicializada
			pos = getLinha("VARIAVEL", 1, var, escopo)
			tabela[pos][6] = 1

		# Percorre fatores da atribuição
		folhas = no_atual.children[1].leaves
		for j in folhas:
			if ("numero" in j.parent.name): # Atribui tipo aos números
				if (j.valor[0].isdigit()):
					j.tipo = ["inteiro"]
				else:
					j.tipo = ["flutuante"]
			pos = getLinha("VARIAVEL", 1, j.valor[0], escopo)
			if ( pos != -1):
				tabela[pos][7] = 1 # Registra que a variável foi utilizada
				if (tabela[pos][6] == 0):
					mensagem = "ERROR: variável " + j.valor[0] + " está sendo usada, mas não foi inicializada."
					lista_mensagens.append(mensagem)
					print(mensagem)
					return -1

	# Percorre filhos
	for i in no_atual.children:
		hasError = percorreArvore(i)
		if (hasError == -1):
			return -1

	# Defina escopo (ao sair da função)
	if ("declaracao_funcao/" in no_atual.name):
		#global escopo
		escopo = "global"



# Faz varredura semântica
def varre_semantica():
	global lista_mensagens
	declaradas = [] # Armazena nome das variaveis declaradas
	repeticoes = [] # Armazena elementos repetidos, para a exclusão
	#print(tabela)

	# === Tem função principal ===
	if (not hasPrincipal()):
		mensagem = "ERROR: Programa não tem função principal."
		lista_mensagens.append(mensagem)
		print(mensagem)
		return -1

	# Percorre tabela de símbolos
	for i in range (len(tabela)):

		# === Verifica se uma variável foi declarada mais de uma vez ===
		if (tabela[i][0] == "VARIAVEL"):
			if (((tabela[i][1]+tabela[i][5]) in declaradas) or ((tabela[i][1]+"global") in declaradas)):
				mensagem = "WARNING: Variável " + tabela[i][1] + " na linha " + str(tabela[i][7]) + " já foi declarada."
				lista_mensagens.append(mensagem)
				print(mensagem)
				repeticoes.append(i)
			else:
				declaradas.append(tabela[i][1]+tabela[i][5])

		# === Olha quantidades de parâmetros das funções ===
		# Encontra as funções
		if (tabela[i][0] == "FUNCAO"):

			# Encontra as chamadas funções
			for j in range (len(tabela)):
				# tabela[i] é a declaração da função, tabela[j] é a chamada da função
				if (tabela[j][0] == "CHAMADA" and tabela[j][1] == tabela[i][1]):
					# Compara se o num de parametros é o mesmo
					if (len(tabela[i][8][1]) != len(tabela[j][8][1])):
								mensagem = "ERROR: A função " + tabela[i][1] + " deve ter " + str(len(tabela[i][8][1]) - 1) + " parâmetros e ela foi chamada com " + str(len(tabela[j][8][1]) - 1) + " parâmetros."
								lista_mensagens.append(mensagem)
								print(mensagem)
								return -1

	# === Remove repeticoes ===
	for i in repeticoes:
		tabela.pop(i)

	# === Percorre Árvore ===
	hasError = percorreArvore(arvore)
	if (hasError == -1):
		return -1

	# === Verifica a inicialização e utilização das variáveis ===
	for i in range (1, len(tabela)):
		# === Verifica se as variáveis foram inicializadas ===
		if (tabela[i][0] == "VARIAVEL" and tabela[i][6] == 0):
			mensagem = "WARNING: Variável " + tabela[i][1] + " na linha " + str(tabela[i][9]) + " foi declarada mas não inicializada."
			lista_mensagens.append(mensagem)
			print(mensagem)

		# === Verifica se as variáveis foram utilizadas ===
		if (tabela[i][0] == "VARIAVEL" and tabela[i][7] == 0):
			mensagem = "WARNING: Variável " + tabela[i][1] + " na linha " + str(tabela[i][9]) + " foi declarada mas nunca utilizada."
			lista_mensagens.append(mensagem)
			print(mensagem)



	#print(tabela)

# Chama varedura
if not tem_erro_yacc:
	has_erros = varre_semantica()

# Poda árvore
poda.poda_arvore(arvore)
#DotExporter(arvore).to_dotfile("arvore_podada.dot")
DotExporter(arvore).to_picture("arvore_podada.png")
#print("Para ver a imagem do grafo em PNG rode \"  dot -Tpng -O arvore_podada.dot \".")

