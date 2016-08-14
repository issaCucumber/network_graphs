#!/usr/bin/python

import xml.sax
import unicodedata
import os
import datetime
import math
import re

from datetime import datetime, date, time

tf = {}
idf = {}
total_docs = 0;
total_words = 0;

def filterText(txt=""):
    #do something
    return True
    

def processText(txt = "", doc_id = ""):
    
    global total_words
    
    words = txt.split()
    
    for word in words:
        
        #TODO: text processing - English detection, auto correction needed, filter unnecessary words
        
        if tf.has_key(word) == False:
            tf[word] = {"frequency" : 1, "docs" : [doc_id]}
        else:
            tf[word]["frequency"] += 1
            if doc_id not in tf[word]["docs"]:
                tf[word]["docs"].add(doc_id) 
    
    total_words += len(words)
        
def generateStats():
    
    #generate new file
    file = open("tfidf/" + datetime.now().__format__("%y%m%d%H%M%%S") + ".txt", "w+")
    file.write("word|tf|total_docs|idf|tf-idf\n")
    
    for word, attr in tf.items():
        tf_value = attr["frequency"]
        total_in_docs = len(attr["docs"])
        idf_value = math.log(total_docs/ total_in_docs)
        tf_idf = tf_value * idf_value
        file.write(word + "|" + str(tf_value) + "|" + str(total_in_docs) + "|" + str(idf_value) + "|" + str(tf_idf) + "\n")
        
    file.close()
    
    
#Post Handler
class PostHandler( xml.sax.ContentHandler ):
    
    def __init__(self):
        self.CurrentData = ""
        self.sentence = ""
        self.id = ""
        
    def startElement(self, name, attrs):
        global tf, idf
        
        self.CurrentData = name
        
        if name == "id":
            self.id = unicodedata.normalize('NFKD', attrs.getValue("id")).encode('ascii','ignore')
        
    def endElement(self, name):
        if name == "content":
            processText(self.sentence, self.id)
        
    def characters(self, content):
        global total_docs
        
        if self.CurrentData == "content":
            self.sentence = unicodedata.normalize('NFKD', content).encode('ascii','ignore')
            total_docs += 1        

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

generateStats()
print "Done processing"