#############################################################
#IMCOMPLETE ORDERING FOR FEEDFORWARD NEURAL NETWORK
#Maybe add a layering function that keeps track of nodes (node order)
#############################################################
"""
https://github.com/neat-python/neat-python/blob/master/neat/population.py
https://github.com/neat-python/neat-python/blob/master/neat/species.py
https://github.com/neat-python/neat-python/blob/master/neat/genome.py
https://github.com/neat-python/neat-python/blob/master/neat/chromosome.py
"""


import math
import random


#Configuration Parameters
edgeEnableMutate = 0.1
edgeWeightDisplaceMutate = 0.1
edgeWeightReplaceMutate = 0.01
edgeWeightDisplaceMagnitude = 0.1
edgeWeightReplaceMagnitude = 1
edgeWeightMax = 2
edgeWeightMin = -2

inputNodeCount = 10
outputNodeCount = 2

nodeAddMutate = 0.1
edgeAddMutate = 0.1

#Node activation functions
def activationFunction(x, activationType):
    if (activationType == 'sigmoid'):
        return 1/(1+math.exp(-x))
    else:
        return 1/(1+math.exp(-x))


#Neuron
class Node:
    def __init__(self, id, nodeType, activationType = 'sigmoid'):
        self.id = id
        self.nodeType = nodeType#'INPUT', 'HIDDEN', 'OUTPUT'
        self.activationType = activationType

    def addEdge(self, edge):
        self.edges.append(edge)

    def copy(self):
        return Node(self.id, self.nodeType, self.activationType)

    def child(self, other):
        #Normally would inherit bias or response randomly between parents
        return Node(self.id, self.nodeType, self.activationType)

#Synapse
class Edge:
    globalInnovationNumber = 0
    innovations = {}
    #inputNode and outputNode are ids
    def __init__(self, inputNode, outputNode, weight, enabled, innovationNumber=None):
        self.inputNode = inputNode
        self.outputNode = outputNode
        self.innovationKey = (inputNode, outputNode)
        self.weight = weight
        self.enabled = enabled
        self.innovationNumber = getNewInnovationNumber(innovationNumber)
    
    @classmethod
    def getNewInnovationNumber(cls, innovationNumber):
        if id is None:
            try:
                self.innovationNumber = self.innovations[self.innovationKey]
            except KeyError:
                cls.globalInnovationNumber += 1
                self.innovationNumber = cls.globalInnovationNumber
                self.innovationNumber[self.innovationKey] = self.innovationNumber
        else:
            return innovationNumber

    def split(self, newNode):
        self.enabled = False
        edge1 = Edge(self.inputNode, newNode, 1.0, True)
        edge2 = Edge(newNode, self.outputNode, self.weight, True)
        return edge1, edge2

    def copy(self):
        return Edge(self.inputNode, self.outputNode, self.weight, self.enabled, self.innovationNumber)

    def child(self, other):
        #AVERAGE WEIGHTS (ONLY CHOOSING RANDOMLY BETWEEN PARENTS RIGHT NOW)
        return random.choice((self,other)).copy()

class NeuralNetwork:
    id = 0
    def __init__(self, parent1=None, parent2=None):
        self.id = getNewId()
        self.inputNodes = []
        self.outputNodes = []

        self.edges = {}
        self.nodes = []
        self.nodeOrder = [] #For Feedforward NeuralNetwork

        for i in range(inputNodeCount):
            node = Node(len(self.nodes), 'INPUT')
            self.inputNodes.append(node)
            self.nodes.append(node)
        for i in range(outputNodeCount):
            node = Node(len(self.nodes), 'OUTPUT')
            self.outputNodes.append(node)
            self.nodes.append(node)

        self.parent1 = parent1
        self.parent2 = parent2
        self.species = None
        self.fitness = 0

    @classmethod
    def getNewId(cls, id):
        cls.id += 1
        return cls.id

    def mutate(self):
        r=random.random
        if r() < nodeAddMutate:
            self.addNode()
        elif r() < edgeAddMutate:
            self.addEdge()
        else:
            for edge in edges:
                edge.mutate()
        return self


    def addNode(self):
        splitEdge = random.choice(self.edges.values())
        newNode = Node(len(self.nodes)+1, 'HIDDEN', 'sigmoid')
        self.nodes.append(newNode)
        edge1, edge2 = splitEdge.split(newNode.id)
        self.edges[edge1.innovationKey]=edge1
        self.edges[edge2.innovationKey]=edge2

        if self.nodes[splitEdge.inputNode-1].nodeType == 'HIDDEN':
            minIndex = self.nodeOrder.index(splitEdge.inputNode)+1
        else:
            minIndex = 0

        if self.nodes[splitEdge.outputNode-1].nodeType == 'OUTPUT':
            maxIndex = self.nodeOrder.index(splitEdge.outputNode)+1
        else:
            maxIndex = len(self.nodeOrder)
        self.nodeOrder.insert(random.randint(minIndex, maxIndex), newNode.id)
        return (newNode, splitEdge)

    def addEdge(self):
        # Add feed forward stuff

    def crossover(self, other):
        parent1 = self
        parent2 = other
        if self.fitness < other.fitness:
            parent1, parent2 = parent1, parent2
            child = NeuralNetwork(self.id, other.id)
            child.inherit(parent1, parent2)
            child.species = parent1.species #parent1 and parent2 should be same species
        return child

    def inherit(child, parent1, parent2):
        for childEdge1 in parent1.edges.values():
            try:
                childEdge2 = parent2.edges.[childEdge1.innovationKey]
            except KeyError:
                child.edges[childEdge1.innovationKey]=childEdge1.copy()
            else:
                if childEdge2.innovationKey == childEdge1.innovationKey:
                    newEdge = childEdge1.child(childEdge2)
                else:
                    newEdge = childEdge1
                child.edges[newEdge.innovationKey]=newEdge
        for i,childNode1 in enumerate(parent1.nodes):
            try:
                child.nodes.append(childNode1.child(parent2.nodes[i]))
            except IndexError:
                child.nodes.append(childNode1.copy())
        child.nodeOrder=parent1.nodeOrder[:]

if __name__ == '__main__':
    print("test")
