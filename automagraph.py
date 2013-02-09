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
from random import randint

# the updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# the pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# the runGraphScript(scriptFile, graph) function can be called to launch another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

def populate(graph, state, delta):
	for n in graph.getNodes():
		state[n] = randint(1,1000)
		delta[n] = 0
	
def pretty(graph, viewColor, viewSize, viewShape, state):
	minDeg = tlp.minDegree(graph)
	maxDeg = tlp.maxDegree(graph)
	deltaDeg = maxDeg - minDeg
	edgeSize = tlp.Size(0.05,0.05,0.05)
	
	for n in graph.getNodes():
		relDeg = 1 - (maxDeg - graph.deg(n))/float(deltaDeg)
		stateSize = relDeg*(state[n])
		viewColor[n] = tlp.Color(40, 40+int(120*relDeg), 180-int(120*relDeg))
		viewSize[n] = tlp.Size(stateSize, stateSize, stateSize)
		viewShape[n] = tlp.NodeShape.Circle
		
	for e in graph.getEdges():
		viewSize[e] = edgeSize
		
def fillDelta(graph, state, delta):
	for n in graph.getNodes():
		deltaN = 0
		for neighbor in tlp.reachableNodes(graph, n, 1):
			nState = state[n]
			neighState = state[neighbor]
			if nState%2 == 0 and neighState%2 == 1 or nState%2 == 0 and neighState%2 == 1:
				temp = nState
				nState = neighState
				neighState = temp
			if nState > neighState:
				deltaN -= 1
			elif nState < neighState:
				deltaN += 1
		delta[n] = deltaN
		
def applyDelta(graph, state, delta, viewSize):
	minDeg = tlp.minDegree(graph)
	maxDeg = tlp.maxDegree(graph)
	deltaDeg = maxDeg - minDeg
	
	for n in graph.getNodes():
		stateN = state[n] + delta[n]
		state[n] = stateN
		relDeg = 1 - (maxDeg - graph.deg(n))/float(deltaDeg)
		stateSize = relDeg*(state[n])
		viewSize[n] = tlp.Size(stateSize, stateSize, stateSize)

def main(graph): 
	viewColor =  graph.getColorProperty("viewColor")
	viewLayout =  graph.getLayoutProperty("viewLayout")
	viewSize =  graph.getSizeProperty("viewSize")
	viewShape = graph.getIntegerProperty("viewShape")
	state = graph.getIntegerProperty("state")
	delta = graph.getIntegerProperty("delta")
	
	populate(graph, state, delta)
	pretty(graph, viewColor, viewSize, viewShape, state)
	pauseScript()
	for t in xrange(100000):
		fillDelta(graph, state, delta)
		applyDelta(graph, state, delta, viewSize)
		updateVisualization(False)
