#!/usr/bin/env

from scipy.io import arff
import sys
from cStringIO import StringIO

class Neuron() :

    def __init__(self) :
	self.output = 0
	# Assume that first input is bias
	self.input = []
	# Assume that first input weight is bias weight
	self.input_weights = []
	self.bias = 0
	self.bias_weight = 0

    def setInput(self, input, input_weights) :
	self.input = input
	self.input_weights = input_weights

    def setBias(self, bias, bias_weight) :
	self.bias = bias
	self.bias_weight = bias_weight

    #def computeOutput(self) :

class NeuralNet() :
    
    #Assuming data and initialWeights have bias appended
    def __init__(self, data, numberOfInputs, initialWeights, bias, bias_weight) :
	self.inputNodes = []
	for i in numberOfInputs :
	    node = Neuron()
	    node.setInput(data[i], '1')
	    self.inputNodes.append(node)
	self.outputNode = Neuron()
	self.outputNode.setBias(bias, bias_weight)


def initialize(data, meta) :
    index = 0
    for i in range(len(meta.names()[:-1])) :
        attr = meta.names()[i]
        if(attr not in attributes) :
            attributes[attr] = []
            attributes_index[attr] = index
            index+=1
        for j in meta.__getitem__(attr)[1] :
             attributes[attr].append(j)
    for i in range(len(data)) :
        instance = data[i]
        if (instance[-1] not in separate_data) :
            separate_data[instance[-1]] = []
            classes.append(instance[-1])
            # Initialize
            class_prob[instance[-1]] = 0
            conditional_prob[instance[-1]] = {}
            conditional_jointprob[instance[-1]] = {}
            jointProb[instance[-1]] = {}
        separate_data[instance[-1]].append(instance)

    totalNum_trainData = len(data) + 2 # Laplace smoothing
    class1_count = len(separate_data[classes[0]]) + 1 # Laplace smoothing
    class2_count = len(separate_data[classes[1]]) + 1
    class_prob[classes[0]] = class1_count / totalNum_trainData
    class_prob[classes[1]] = class2_count / totalNum_trainData


def read_arff(file) :
    f = open(file)
    content = StringIO(f.read())
    data, meta = arff.loadarff(content)
    return data, meta


def main(args) :
    data, meta = read_arff(args)
    print data
    print 'akjgladgbj'
    print meta

if __name__ == "__main__":
    main(sys.argv[1])

