#!/usr/bin/python

import xml.sax
import unicodedata
import os
import size
import color

from graph_tool.all import *

vertices = {}
g = Graph(directed=False)
v_color = g.new_vertex_property("int")
v_size  = g.new_vertex_property("int")

#Post Handler
class PostHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.dataStruct = []
        self.commentLevel = 0
        
    def startElement(self, name, attrs):
        global vertices
        
        if name == "post":
            replyto = unicodedata.normalize('NFKD', attrs.getValue("replyto")).encode('ascii','ignore')
            id = unicodedata.normalize('NFKD', attrs.getValue("id")).encode('ascii','ignore')
            
            #generate vertex of the current post id
            if vertices.has_key(id) == False:
                vertices[id] = g.add_vertex()
            
            if vertices.has_key(replyto) == False:
                vertices[replyto] = g.add_vertex()
            
            if replyto == "null":
                g.add_edge(vertices["human_rights"], vertices[id])
                v_color[vertices[id]] = color.LEVEL_1
                v_size[vertices[id]] = size.ROOT - 10
            else:
                g.add_edge(vertices[replyto], vertices[id])
                v_color[vertices[id]] = color.LEVEL_1 + self.commentLevel
                v_size[vertices[id]] = size.ROOT - 10 * (1 + self.commentLevel)
                
        
        if name == "comments":
            self.commentLevel += 1
        
    def endElement(self, name):
        
        if name == "comments":
            self.commentLevel -= 1
#         self.CurrentData = name
#         if name == "comment":
#             self.CommentFlag = True
        
#     def characters(self, content):
#         if self.CurrentData == "post":
#             if self.CommentFlag:          


#add the root vertex to the graph (topic)
vertices["human_rights"] = g.add_vertex()
v_color[vertices["human_rights"]] = color.ROOT
v_size[vertices["human_rights"]] = size.ROOT
 
#create reader
parser = xml.sax.make_parser()
parser.setFeature(xml.sax.handler.feature_namespaces, 0)

# override the default ContextHandler
Handler = PostHandler()
parser.setContentHandler( Handler )

dirname = "data/"
for f in os.listdir(dirname):
    xmlfile = os.path.join(dirname, f)
    if os.path.isfile(xmlfile):
        parser.parse(xmlfile)

g.vertex_properties["color"] = v_color
g.vertex_properties["size"] = v_size

pos = sfdp_layout(g)
graph_draw(g, pos, 
           vertex_fill_color=v_color,
           vertex_font_size=10, 
           vertex_size=v_size, 
           edge_pen_width=1.2,
           output_size=(1000, 1000),
           output="human_rights.png")
    