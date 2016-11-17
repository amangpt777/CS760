#!/usr/bin/env

from scipy.io import arff
import sys
from cStringIO import StringIO
import math
import random

classData = {}
separate_data = {}
classes = []
attributes = {}
attributes_index = {}

class Neuron() :

    def __init__(self) :
	self.output = 0
	self.outputVal = 0
	# Assume that first input is bias
	self.input = []
	# Assume that first input weight is bias weight
	self.input_weights = []
	self.bias = 0.5
	self.bias_weight = 0

    def setInput(self, input, input_weights) :
	self.input = input
	self.input_weights = input_weights

    def setBias(self, bias, bias_weight) :
	self.bias = bias
	self.bias_weight = bias_weight

    def computeOutput(self) :
	weighted_sum = 0
	for i in range(len(self.input)) :
	    weighted_sum += self.input[i] * self.input_weights[i]
	weighted_sum += self.bias * self.bias_weight
	self.outputVal = 1 / (1 + math.exp(-weighted_sum))
	if (self.outputVal >= 0.5) :
	    self.output = 1
	else :
	    self.output = 0


class InputNeuron(Neuron) :
    def __init__(self) :
	Neuron.__init__(self)

    def setInput(self, input, weight) :
	self.input = input
	self.input_weight = weight
    
    def computeOutput(self) :
	self.output = self.input
	self.outputVal = self.input


class OutputNeuron(Neuron) :
    pass

class NeuralNet() :
    
    #Assuming data and initialWeights have bias appended
    def __init__(self, data, initialWeights, bias, bias_weight) :
	self.inputNodes = []
	for i in range(len(data)) :
	    #print "Initialize input neuron"
	    #print data[i]
	    node = InputNeuron()
	    #node.setInput(data[i])
	    node.setInput(data[i], initialWeights[i])
	    node.computeOutput()
	    self.inputNodes.append(node)
	self.outputNode = OutputNeuron()
	self.outputNode.setBias(bias, bias_weight)
	self.outputNode.setInput(data, initialWeights)


def trainNNet(net, actualClass, learnRate) :
    weightMatrix = []
    net.outputNode.computeOutput()
    o = net.outputNode.outputVal
    delta = o * (1 - o) * (actualClass - o)
    for i in range(len(net.inputNodes)) :
	#print learnRate
	#print delta
	#print net.outputNode.input
	#print net.outputNode.input_weights
	updatedWeight = net.inputNodes[i].input_weight + learnRate * delta * net.inputNodes[i].input
	weightMatrix.append(updatedWeight)
	net.inputNodes[i].setInput(net.inputNodes[i].input, updatedWeight)

    #print net.outputNode.input
    #print net.outputNode.input_weights
    updated_bias_weight = net.outputNode.bias_weight + learnRate * delta * net.outputNode.bias
    #print o
    return weightMatrix, updated_bias_weight
    
def initialize(data, meta) :
    index = 0
    for i in range(len(data)) :
        instance = data[i].tolist()
        if (instance[-1] not in separate_data) :
            separate_data[instance[-1]] = []
            classes.append(instance[-1])
        separate_data[instance[-1]].append(instance)

def createFolds(data, meta, num_folds) :
    folds = [None]*num_folds
    #print len(classes)
    for i in range(len(classes)) :
	#print i
	#print separate_data[classes[i]]
        random.sample(separate_data[classes[i]], len(separate_data[classes[i]]))
	eachFold = len(separate_data[classes[i]]) / num_folds
	counter = 0
	j = 0
	for j in range(num_folds) :
	    if folds[j] is None :
		folds[j] = []
	    #print separate_data[classes[i]][counter : eachFold - 1]
	    for m in range(counter, counter + eachFold) :
		folds[j].append(separate_data[classes[i]][m])
	    counter = counter + eachFold
	remains = len(separate_data[classes[i]]) % num_folds
	#print remains
	counter = eachFold * num_folds
	for j in range(remains) :
	    if folds[j] is None :
                folds[j] = []
	    folds[j].append(separate_data[classes[i]][counter])
	    counter = counter + 1

    return folds
	


def read_arff(file) :
    f = open(file)
    content = StringIO(f.read())
    data, meta = arff.loadarff(content)
    return data, meta



def main(args) :
    data, meta = read_arff(args[0])
    print len(data)
    num_folds = int(args[1])
    learning_rate = float(args[2])
    num_epochs = int(args[3])
    initialize(data, meta)
    folds = createFolds(data, meta, num_folds)
    #print folds
    #print len(folds)

    initialWeights = []
    inputs = []
    instance = data[0]
    #print instance
    #print type(instance)
    #print instance.tolist()
    instance = instance.tolist()
    inputs = instance[0:len(data[0])-1]
    inputs = map(float, inputs)
    #i = 0
    #print inputs
    for i in range(len(inputs)) :
        initialWeights.append(0.1)
    bias = 0.5
    bias_weight = 0.1
    net = NeuralNet(inputs, initialWeights, bias, bias_weight)

    leave = 0
    weight = initialWeights
#    for i in range(num_epochs) :
    accurate = 0
    while leave != num_folds :
	correctClassify = 0
	#while leave != num_folds :
	for i in range(num_epochs) :
	    for j in range(len(folds)) :
	        if j == leave :
		    continue
	        if leave == num_folds :
		    break
	        myData = random.sample(folds[j], len(folds[j]))
	    #print "Fold j is"
	    #print myData
	    #print 'length is'
	    #print len(myData)
	        for k in range(len(myData)) :
		    y = 0
		#print 'class is'
		#print myData[k][-1]
		    if myData[k][-1] == 'Rock' :
		    #print 'Rock'
		        y = 0
		    if myData[k][-1] == 'Mine' :
		    #print 'Mine'
		        y = 1
		#change input
		    instance = myData[k]
		    inputs = instance[0:len(instance)-1]
		#print y
		    inputs = map(float, inputs)
		    net = NeuralNet(inputs, weight, bias, bias_weight)
		    weight, bias_weight = trainNNet(net, y, learning_rate)
		    #print inputs
		    #print weight
		    #print 'Hello'
	testSet = folds[leave]
	for k in range(len(testSet)) :
	    instance = testSet[k]
            inputs = instance[0:len(instance)-1]
            #print inputs
            inputs = map(float, inputs)
            net = NeuralNet(inputs, weight, bias, bias_weight)
	    net.outputNode.computeOutput()
            o = net.outputNode.outputVal
	    predictedClass = net.outputNode.output
	    actualClass = instance[-1]
	    print leave, predictedClass, actualClass, o
	    if predictedClass == 0 and actualClass == 'Rock':
		accurate = accurate + 1
	    if predictedClass == 1 and actualClass == 'Mine':
                accurate = accurate + 1

	#testNet()
	leave = leave + 1
	
    print accurate
    #trainNNet(net, 1, 0.1)

if __name__ == "__main__":
    main(sys.argv[1:])

