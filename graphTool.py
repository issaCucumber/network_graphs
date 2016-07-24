from graph_tool.all import *

g = Graph(directed=False)
v1 = g.add_vertex()
v2 = g.add_vertex()
v3 = g.add_vertex()
v4 = g.add_vertex()

e1 = g.add_edge(v1, v2)
e2 = g.add_edge(v1, v3)
e3 = g.add_edge(v1, v4)

pos = sfdp_layout(g)
graph_draw(g, pos,
           vertex_text=g.vertex_index, 
           vertex_font_size=10, vertex_size=1, edge_pen_width=1.2,
           output_size=(500, 500))