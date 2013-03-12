
##############################
# Kirby Banman
# 
# Usage examples for rdflib methods:
#   serialize()	- line 31
#   encode()	- line 57-59
#   Namespace() - line 78
# 
# Run with command:
#   $ python rdflibTest.py
# 
# Creates file:
#   einst.rdf
# 
# Tested with python 2.7 on Ubuntu 12.04 LTS
##############################


import rdflib

# next 3 lines dereference the rdf document that dbpedia
# hosts for einstein, loading it into an rdflib.Graph() object
uri = "http://dbpedia.org/resource/Albert_Einstein"
rdfGraph = rdflib.Graph()
rdfGraph.load(uri)

# this is how to save the rdf document to a file in rdflib's
# default format (rdf-xml) using the serialize() method.
# (does not affect the rest of the program in any way)
rdfGraph.serialize("einst.rdf")

# get the choice from the user
print "enter T to see every triple"
print "enter C to see just the rdfs:comment triples"
print "enter A to see just the dbpedia-owl:abstract triples"
userChoice = raw_input("choice? ")


# counter for triples printed
triples = 0

####################
# PRINT EVERY TRIPLE
####################

if userChoice.lower() == "t":
	# the following loop prints the content of each triple in the
	# dereferenced graph
	for s,p,o in rdfGraph:
		# next 3 lines encode the strings subject and object as
		# UTF-8 strings.
		# s, p, and o are all rdflib.Node objects, which have the
		# encode() method.
		# UTF-8 is chosen because the rdf-xml document header for
		# einstein example is <?xml version="1.0" encoding="utf-8" ?>
		sContent = s.encode("UTF-8")
		pContent = p.encode("UTF-8")
		oContent = o.encode("UTF-8")

		# next 6 lines print the triples in a nice format
		triples += 1
		print "TRIPLE " + str(triples) + ":"
		print "  SUBJECT:\n\t" + sContent
		print "  PREDICATE:\n\t" + pContent
		print "  OBJECT:\n\t" + oContent + "\n"


##########################
# PRINT EVERY RDFS:COMMENT
##########################

elif userChoice.lower() == "c":
	# print the triples containing the predicate rdfs:comment
	# from the einstein document using rdflib's namespace functionality.
	# the Namespace() method returns an rdflib.URIRef object, which
	# inherits from the rdflib.Node object.
	rdfs = rdflib.Namespace("http://www.w3.org/2000/01/rdf-schema#")
	
	# the following loop prints each triple with rdfs:comment
	# the subject_objects method returns an iterator over subject, object
	# tuples containing the specified predicate.
	for s,o in rdfGraph.subject_objects(rdfs.comment):
		# again, UTF-8 encoding is used.
		# the predicate is left out here because we specified it and
		# don't need to specify its encoding format.
		sContent = s.encode("UTF-8")
		oContent = o.encode("UTF-8")

		# next 6 lines print the triples in a nice format
		triples += 1
		print "TRIPLE " + str(triples) + ":"
		print "  SUBJECT:\n\t" + sContent
		print "  PREDICATE:\n\t" + rdfs.comment
		print "  OBJECT:\n\t" + oContent + "\n"

	
##################################
# PRINT EVERY DBPEDIA-OWL:ABSTRACT
##################################
	
elif userChoice.lower() == "a":
	# print the triples containing the predicate dbpedia-owl:abstract
	# from the einstein document directly using an rdflib.URIRef object
	dbpedia_owl_abstract = rdflib.URIRef("http://dbpedia.org/ontology/abstract")

	# this is exactly analogous to the previous block of code that printed
	# rdfs:comment triples
	for s,o in rdfGraph.subject_objects(dbpedia_owl_abstract):
		sContent = s.encode("UTF-8")
		oContent = o.encode("UTF-8")

		triples += 1
		print "TRIPLE " + str(triples) + ":"
		print "  SUBJECT:\n\t" + sContent
		print "  PREDICATE:\n\t" + dbpedia_owl_abstract
		print "  OBJECT:\n\t" + oContent + "\n"


# print the uri again, and repeat how many triples were printed
print "\n\n FROM URI " + uri + ":\n"
print "    " + str(triples) + " TRIPLES PRINTED.\n\n"

