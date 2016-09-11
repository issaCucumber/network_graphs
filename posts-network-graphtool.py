#!/usr/bin/python

import xml.sax
import unicodedata
import os
import size
import color
import re

from graph_tool.all import *
from numpy import integer

vertices = {}
g = Graph(directed=False)
v_color = g.new_vertex_property("int")
v_size  = g.new_vertex_property("int")
v_pen_width = g.new_vertex_property("int")

regex = re.compile(r"[0-9]+k*")

#Post Handler
class PostHandler( xml.sax.ContentHandler ):
    def __init__(self):
        self.dataStruct = []
        self.commentLevel = 0
        self.currentData = ""
        self.currentPostVertexId = 0
        
    def startElement(self, name, attrs):
        global vertices
        
        self.currentData = name
        
        if name == "post":
            replyto = unicodedata.normalize('NFKD', attrs.getValue("replyto")).encode('ascii','ignore')
            id = unicodedata.normalize('NFKD', attrs.getValue("id")).encode('ascii','ignore')
            
            #generate vertex of the current post id
            if vertices.has_key(id) == False:
                vertices[id] = g.add_vertex()
                self.currentPostVertexId = vertices[id]
            
            if vertices.has_key(replyto) == False:
                vertices[replyto] = g.add_vertex()
                self.currentPostVertexId = vertices[replyto]
            
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
        
    def characters(self, content):
        if self.currentData == "reaction":
            
            reaction = unicodedata.normalize('NFKD', content).encode('ascii','ignore')
            matches = regex.match(reaction)
            
            if matches:
                match = matches.group(0)
                match_arr = match.split('k')[0]
                if len(match_arr) == 2:
                   reaction = int(match_arr[0]) * 1000 
                else:
                   reaction = int(match_arr[0])  
                
            else:
                reaction = 0

            if reaction == 0:
                v_pen_width[self.currentPostVertexId] = 0.5
            else:
                v_pen_width[self.currentPostVertexId] = reaction * 0.01

#add the root vertex to the graph (topic)
vertices["human_rights"] = g.add_vertex()
v_color[vertices["human_rights"]] = color.ROOT
v_size[vertices["human_rights"]] = size.ROOT
v_pen_width[vertices["human_rights"]] = 1.2
 
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
g.vertex_properties["pen_width"] = v_pen_width

pos = sfdp_layout(g)
graph_draw(g, pos, 
           vertex_fill_color=v_color,
           vertex_font_size=10, 
           vertex_size=v_size, 
           vertex_pen_width = v_pen_width,
           edge_pen_width=1.2,
           output_size=(1000, 1000))
    