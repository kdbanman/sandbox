# Powered by Python 2.5

#
# library imports
#
from tulip import *
from tulipogl import *
from tulipgui import *

#
# graph initialization and configuration
#
graph = tlp.newGraph()
environment = graph.addSubGraph()

gApproxParams = tlp.getDefaultPluginParameters("Grid Approximation", \
                environment)
gApproxParams["degree"] = 10
gApproxParams["nodes"] = 600
gApproxParams["long edge"] = False
tlp.importGraph("Grid Approximation", gApproxParams, environment)

#
# relevant graph parameters
#
viewColor =  graph.getColorProperty("viewColor")
viewLayout =  graph.getLayoutProperty("viewLayout")
viewSelection =  graph.getBooleanProperty("viewSelection")
viewShape =  graph.getIntegerProperty("viewShape")
viewSize =  graph.getSizeProperty("viewSize")
#current state of node, D=0,B=1,R=2,G=3
nodeState = graph.getIntegerProperty("nodeState")
#for storage of next state, same as above
nodeNext = graph.getIntegerProperty("nodeNext")
#for pre-iteration state choosers
currentChoice = graph.getIntegerProperty("currentChoice")

#
# layout for environment graph
#
layoutParams = tlp.getDefaultPluginParameters("FM^3 (OGDF)", environment)
environment.applyLayoutAlgorithm("FM^3 (OGDF)", viewLayout, layoutParams)

#
# node menu of state choosers and start button
#
choosers = graph.addSubGraph()
chooseSize = tlp.Size(50,20,1)
chooseY = -tlp.computeBoundingBox(graph).height()/2.0 - 20.0
chooseX = -tlp.computeBoundingBox(graph).width()/2.0 + 25.0
center = tlp.computeBoundingBox(graph).center()
viewColor.setAllNodeValue(tlp.Color(0,0,0))

chooseDead = choosers.addNode()
viewColor[chooseDead] = tlp.Color(0,0,0)
viewLayout[chooseDead] = tlp.Coord(center + tlp.Vec3f(chooseX,chooseY,0.0))
viewSize[chooseDead] = chooseSize
nodeState[chooseDead] = 0

chooseBlue = choosers.addNode()
viewColor[chooseBlue] = tlp.Color(0,0,255)
viewLayout[chooseBlue] = tlp.Coord(center + \
                                   tlp.Vec3f(chooseX+55.0,chooseY,0.0))
viewSize[chooseBlue] = chooseSize
nodeState[chooseBlue] = 1

chooseRed = choosers.addNode()
viewColor[chooseRed] = tlp.Color(255,0,0)
viewLayout[chooseRed] = tlp.Coord(center + \
                                  tlp.Vec3f(chooseX+110.0,chooseY,0.0))
viewSize[chooseRed] = chooseSize
nodeState[chooseRed] = 2

chooseGreen = choosers.addNode()
viewColor[chooseGreen] = tlp.Color(0,255,0)
viewLayout[chooseGreen] = tlp.Coord(center + \
                                    tlp.Vec3f(chooseX+165.0,chooseY,0.0))
viewSize[chooseGreen] = chooseSize
nodeState[chooseGreen] = 3

chooseStart = choosers.addNode()
viewColor[chooseStart] = tlp.Color(180,255,180)
viewLayout[chooseStart] = tlp.Coord(center + \
                                    tlp.Vec3f(chooseX+240.0,chooseY,0.0))
viewSize[chooseStart] = chooseSize
viewShape[chooseStart] = tlp.NodeShape.Circle

chooseStep = choosers.addNode()
viewColor[chooseStep] = tlp.Color(255,255,180)
viewLayout[chooseStep] = tlp.Coord(center + \
                                   tlp.Vec3f(chooseX+295.0,chooseY,0.0))
viewSize[chooseStep] = chooseSize
viewShape[chooseStep] = tlp.NodeShape.Circle

#
# gui init and config
#
tlp.closeAllViews()
view = tlp.addNodeLinkDiagramView(graph)
view.setOptionsWidgetsVisible(False)

#
# functions for computing next graph state and state transition
#
def computeNext(env):
    for n in env.getNodes():
        blueNbr = False
        redNbr = False
        greenNbr = False
        for nbr in env.getInOutNodes(n):
            nbrState = nodeState[nbr]
            if not blueNbr:
                blueNbr = nbrState == 1
            if not redNbr:
                redNbr = nbrState == 2
            if not greenNbr:
                greenNbr = nbrState == 3
        if (not blueNbr and not redNbr and not greenNbr) or \
           (blueNbr and redNbr and greenNbr):
            nodeNext[n] = 0
        elif (not blueNbr and not redNbr and greenNbr) or \
             (not blueNbr and redNbr and greenNbr):
            nodeNext[n] = 3
        elif (not blueNbr and redNbr and not greenNbr) or \
             (blueNbr and redNbr and not greenNbr):
            nodeNext[n] = 2
        elif (blueNbr and not redNbr and not greenNbr) or \
             (blueNbr and not redNbr and greenNbr):
            nodeNext[n] = 1

def iterate(env):
    for n in env.getNodes():
        nodeState[n] = nodeNext[n]

def run(env,v,obs):
    while obs.started:
        computeNext(env)
        iterate(env)
        v.draw()
        if obs.stepping:
            obs.stepping = False
            obs.started = False

#
# event handlers for node selection and color response
#
class SelectObserver(tlp.PropertyObserver):
    started = False
    stepping = False
    def afterSetNodeValue(self, viewSelection, node):
        if node in choosers.getNodes():
            if node == chooseStart:
                if not self.started:
                    self.started = True
                    viewColor[node] = tlp.Color(255,180,180)
                    run(environment,view,self)
                else:
                    self.started = False
                    viewColor[node] = tlp.Color(180,255,180)
            elif node == chooseStep:
                self.started = True
                self.stepping = True
                run(environment,view,self)
            else:
                currentChoice.setAllNodeValue(nodeState[node])
        else:
		    nodeState[node] = currentChoice[node]

class ColorResponder(tlp.PropertyObserver):
    _black = tlp.Color(0,0,0)
    _blue = tlp.Color(0,0,255)
    _red = tlp.Color(255,0,0)
    _green = tlp.Color(0,255,0)
    def afterSetNodeValue(self, nodeState, node):
        s = nodeState[node]
        if s == 1:
            viewColor[node] = self._blue
        elif s == 2:
            viewColor[node] = self._red
        elif s == 3:
            viewColor[node] = self._green
        else:
            viewColor[node] = self._black
            
#
# observer initialization
#
selectObserver = SelectObserver()
colorResponder = ColorResponder()
viewSelection.addPropertyObserver(selectObserver)
nodeState.addPropertyObserver(colorResponder)
