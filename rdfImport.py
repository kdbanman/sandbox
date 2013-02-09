from tulip import *
from math import *
from random import *
from collections import deque
import rdflib

def importURI(graph, uri="http://dbpedia.org/resource/Albert_Einstein"): 
	viewBorderColor =  graph.getColorProperty("viewBorderColor")
	viewBorderWidth =  graph.getDoubleProperty("viewBorderWidth")
	viewColor =  graph.getColorProperty("viewColor")
	viewFont =  graph.getStringProperty("viewFont")
	viewFontSize =  graph.getIntegerProperty("viewFontSize")
	viewLabel =  graph.getStringProperty("viewLabel")
	viewLabelColor =  graph.getColorProperty("viewLabelColor")
	viewLabelPosition =  graph.getIntegerProperty("viewLabelPosition")
	viewLayout =  graph.getLayoutProperty("viewLayout")
	viewMetaGraph =  graph.getGraphProperty("viewMetaGraph")
	viewRotation =  graph.getDoubleProperty("viewRotation")
	viewSelection =  graph.getBooleanProperty("viewSelection")
	viewShape =  graph.getIntegerProperty("viewShape")
	viewSize =  graph.getSizeProperty("viewSize")
	viewSrcAnchorShape =  graph.getIntegerProperty("viewSrcAnchorShape")
	viewSrcAnchorSize =  graph.getSizeProperty("viewSrcAnchorSize")
	viewTexture =  graph.getStringProperty("viewTexture")
	viewTgtAnchorShape =  graph.getIntegerProperty("viewTgtAnchorShape")
	viewTgtAnchorSize =  graph.getSizeProperty("viewTgtAnchorSize")

	content = graph.getStringProperty("content")
	rdfType = graph.getStringProperty("rdfType")
	
	rdfGraph = rdflib.Graph()
	rdfGraph.load(uri)

	triples = 0
	for s,p,o in rdfGraph:
		
		# Add subject and object to tulip graph, testing to see if either
		# already exists
		sContent = s.encode("UTF-8")
		oContent = o.encode("UTF-8")
		
		newS = True
		newO = True
		for n in graph.getNodes():
			nContent = content[n]
			if nContent == sContent:
				sNode = n
				newS = False
			if nContent == oContent:
				oNode = n
				newO = False
				
		if newS:
			sNode = graph.addNode()
			content[sNode] = sContent
		if newO:
			oNode = graph.addNode()
			content[oNode] = oContent
			
		
		# Change shape based on literal or URI content
		if newS:
			if type(s) == rdflib.URIRef:
				rdfType[sNode] = "URI"
				viewShape[sNode] = tlp.NodeShape.Circle
				viewColor[sNode] = tlp.Color(20,20,100)
			elif type(s) == rdflib.Literal:
				rdfType[sNode] = "Literal"
				viewShape[sNode] = tlp.NodeShape.Square
				viewColor[sNode] = tlp.Color(100,20,20)
			else:
				print "ERROR: rdf nodes must be URIs or Literals"
				print content[sNode]
		if newO:
			if type(o) == rdflib.URIRef:
				rdfType[oNode] = "URI"
				viewShape[oNode] = tlp.NodeShape.Circle
				viewColor[oNode] = tlp.Color(10,10,100)
			elif type(o) == rdflib.Literal:
				rdfType[oNode] = "Literal"
				viewShape[oNode] = tlp.NodeShape.Square
				viewColor[oNode] = tlp.Color(100,10,10)
			else:
				print "ERROR: rdf nodes must be URIs or Literals"
				print content[oNode]
		
		# Connect the subject to the object with the predicate
		pEdge = graph.addEdge(sNode, oNode)
		content[pEdge] = p.encode("UTF-8")
		
		triples += 1
	
	print str(triples) + " triples successfully loaded into tulip graph for\n " + uri + "\n\n"

##
##  MAIN
##

def main(graph): 

	#mportURI(graph, "http://dbpedia.org/resource/Donald_Knuth")
	importURI(graph, "http://dbpedia.org/resource/Linus_Torvalds")
	importURI(graph, "http://dbpedia.org/resource/Alan_Cox")
	importURI(graph, "http://dbpedia.org/resource/Bill_Gates")
	importURI(graph, "http://dbpedia.org/resource/Rich_Hickey")
	importURI(graph, "http://dbpedia.org/resource/Alan_Kay")
	importURI(graph, "http://dbpedia.org/resource/Richard_Stallman")
	
	
