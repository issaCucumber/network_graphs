#!/usr/bin/python

import xml.sax
import unicodedata
import os

import networkx as nx
import matplotlib.pyplot as plt

dataSet = []

#graw graph
def draw_graph(graph):

    # extract nodes from graph
    nodes = set([n1 for n1, n2 in graph] + [n2 for n1, n2 in graph])

    # create networkx graph
    G=nx.Graph()

    # add nodes
    for node in nodes:
        G.add_node(node)

    # add edges
    for edge in graph:
        G.add_edge(edge[0], edge[1])

    # draw graph
    pos = nx.spectral_layout(G)
    nx.draw(G, pos)

    # show graph
    plt.show()

#Post Handler
class PostHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.dataStruct = []
        
    def startElement(self, name, attrs):
        global dataSet
        
        if name == "post":
            replyto = unicodedata.normalize('NFKD', attrs.getValue("replyto")).encode('ascii','ignore')
            id = unicodedata.normalize('NFKD', attrs.getValue("id")).encode('ascii','ignore')
            if replyto == "null":
                dataSet.append(("human_rights", id))
            else:
                dataSet.append((replyto, id))
                
            
        
#         self.CurrentData = name
#         if name == "comment":
#             self.CommentFlag = True
        
#     def characters(self, content):
#         if self.CurrentData == "post":
#             if self.CommentFlag:          
    
#create reader
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = PostHandler()
parser.setContentHandler( Handler )

dirname = "data/"
for f in os.listdir(dirname)[:10]:
    xmlfile = os.path.join(dirname, f)
    if os.path.isfile(xmlfile):
        parser.parse(xmlfile)
    
        
draw_graph(dataSet)
    