from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from yacc_tzora import arvore, tabela

def hasPrincipal():
	has = False
	for i in tabela:
		if ("principal" in i):
			has = True
	return has

def varre_semantica():
	lista_mensagens = []
	#print(tabela)

	# Tem função principal
	if (not hasPrincipal()):
		lista_mensagens.append("ERRO: Programa não tem função principal.")
		print("ERRO: Programa não tem função principal.")
		return -1

	# Olha quantidades de parâmetros
	for i in range (len(tabela)):
		if (tabela[i][0] == "FUNCAO"):
			print("funcao")
	FAZER ESSA REGRA
	COMPARAR DADOS DA TABELA

varre_semantica()

