from anytree import Node, RenderTree
from anytree.exporter import DotExporter

udo = Node("Udo")
marc = Node("Marc", parent=udo)
lian = Node("Lian", parent=marc)
dan = Node("Dan", parent=udo)
jet = Node("Jet", parent=dan)
jan = Node("Jan", parent=dan)
joe = Node("Joe", parent=dan)

s0 = Node("sub0", parent=None, children=[udo])


# graphviz needs to be installed for the next line!
DotExporter(s0).to_picture("s0.png")
