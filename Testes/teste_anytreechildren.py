from anytree import Node, RenderTree
from anytree.exporter import DotExporter

joe = Node("Joe")
jan = Node("Jan", children=[joe])
jet = Node("Jet", children=[jan])
dan = Node("Dan", children=[jet])
lian = Node("Lian", children=[dan])
marc = Node("Marc", children=[lian])
udo = Node("Udo", children=[marc])

#s0 = Node("sub0", parent=None, children=[udo])


# graphviz needs to be installed for the next line!
DotExporter(udo).to_picture("udo_children.png")
