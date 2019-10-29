from anytree import Node, RenderTree
from anytree.exporter import DotExporter

from yacc_tzora import arvore

DotExporter(arvore).to_picture("teste.png")
