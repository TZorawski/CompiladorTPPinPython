from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from yacc_tzora import arvore, tabela

def varre_semantica ():
	lista_mensagens = []
	if (arvore.children[0].children[0].children[0].children[1].children[0].valor[0] != "principal"):
		lista_mensagens.append("ERRO: Programa não tem função principal.")
		print("ERRO: Programa não tem função principal.")
		return -1

varre_semantica()

CORRIGIR TIPO IF
