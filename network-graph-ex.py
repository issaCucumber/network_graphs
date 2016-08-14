import networkx as nx
import matplotlib.pyplot as plt

def draw_graph(graph):
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])
    
    G = nx.Graph()
    
    #add edge
    G.add_edges_from(graph)
    
#     for node in nodes:
#         G.add_node(node)
        
     # draw graph
    pos = nx.shell_layout(G)
    nx.draw(G, pos, with_labels=True)

    # show graph
    plt.axis('off')
    plt.show()
    
# draw example
graph = [(20, 21),(21, 22),(22, 23), (23, 24),(24, 25), (25, 20)]
draw_graph(graph)