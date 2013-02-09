# Powered by Python 2.5

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import *

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# the main(graph) function must be defined 
# to run the script on the current graph

def main(graph): 
	gid =  graph.getDoubleProperty("gid")
	lastaccess =  graph.getDoubleProperty("lastaccess")
	lastchange =  graph.getDoubleProperty("lastchange")
	lastmodif =  graph.getDoubleProperty("lastmodif")
	name =  graph.getStringProperty("name")
	path =  graph.getStringProperty("path")
	size =  graph.getDoubleProperty("size")
	uid =  graph.getDoubleProperty("uid")
	url =  graph.getStringProperty("url")
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


	fileSize = graph.getDoubleProperty("size")
	lastAccess = graph.getDoubleProperty("lastaccess")
	
	n_count = 0	
	for n in graph.getNodes():
		
		# the taller the node, the larger the filesize
		nodeFileSize = fileSize.getNodeValue(n)
		# scale file size to reasonable magnitude with a minimum of 0.5
		height = 0.5 + nodeFileSize/1000000.0
		viewSize[n] = tlp.Size(2,3.0*height,1)
				
		nodeLastAccess = lastAccess.getNodeValue(n)
		# scale relative file size between zero and one
		Scale = (nodeLastAccess - 1320000000.0) / 35000000.0
		# the greener the node, the older its access time
		newColor = tlp.Color(int(128*Scale), int(255 - 255*Scale), int(255*Scale))
		viewColor[n] = newColor
		
		
		n_count+=1
	
	e_count = 0	
	for e in graph.getEdges():
		
		e_count+=1
		
		
	print "height now scaled to file size for " + str(n_count) + " files and " + str(e_count) + " nodes."
	
	
		
		
