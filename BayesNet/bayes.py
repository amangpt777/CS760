#!/usr/bin/env


from __future__ import division
import sys
from scipy.io import arff
from cStringIO import StringIO
from random import randint
import math
import matplotlib.pyplot as plt

conditional_prob = {}
class_prob = {}
separate_data = {}
classes = []
attributes = {}
attributes_index = {}
laplace = 1

#For TAN
CMI = {}
conditional_jointprob = {}
jointProb = {}
V_new = []
E_new = []
CPT = {}
root = []



def read_arff(file) :
    f = open(file)
    content = StringIO(f.read())
    data, meta = arff.loadarff(content)
    return data, meta




#Initializes attributes, attributes_index, separate_data, classes, class_prob, conditional_prob, separate_data
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




# Calculates and fills in the conditional probabilies in dicitonary -> conditional_prob
def calculate_conditional_prob(data, meta) :
    for i in range(len(classes)) :
	subset_classData = separate_data[classes[i]]
	for attr in meta.names()[:-1] :
	    conditional_prob[classes[i]][attr] = {}
	    for attr_value in attributes[attr] :
		count_attr_val = 0
		for j in range(len(subset_classData)) :
		    if(subset_classData[j][attributes_index[attr]] == attr_value) :
			count_attr_val += 1
		numerator = count_attr_val + 1   #Laplace smoothing
		denominator = len(subset_classData) + len(attributes[attr])
		conditional_prob[classes[i]][attr][attr_value] = numerator / denominator





# Calculates conditional joint probability and joint probability
def calculate_requiredProb(data, meta) :
    for k in range(len(classes)) :
        for attr_1 in meta.names()[:-1] :
	    CMI[attr_1] = {}
	    jointProb[classes[k]][attr_1] = {}
	    conditional_jointprob[classes[k]][attr_1] = {}
            for attr_2 in meta.names()[:-1] :
		denominator_condJointProb = len(separate_data[classes[k]]) + (len(attributes[attr_1]) * len(attributes[attr_2]))# * len(classes))
		denominator_jointProb = len(data) + (len(attributes[attr_1]) * len(attributes[attr_2]) * len(classes))
                if (attr_1 == attr_2) :
                    CMI[attr_1][attr_2] = -1
                else :
		    matrix_condJointProb = []
		    matrix_jointProb = []
                    for attr_1_val in attributes[attr_1] :
			temp_list_condJointProb = []
			temp_list_jointProb = []
                        for attr_2_val in attributes[attr_2] :
			    counter_condJointProb = 0
			    counter_jointProb = 0
                            for instance in separate_data[classes[k]] :
                                if(instance[attributes_index[attr_1]] == attr_1_val and instance[attributes_index[attr_2]] == attr_2_val and instance[-1] == classes[k]) :
                                    counter_condJointProb += 1
			    temp_list_condJointProb.append((counter_condJointProb + 1) / denominator_condJointProb)
			    for instance in data :
				if(instance[attributes_index[attr_1]] == attr_1_val and instance[attributes_index[attr_2]] == attr_2_val and instance[-1] == classes[k]) :
                                    counter_jointProb += 1
			    temp_list_jointProb.append((counter_jointProb + 1) / denominator_jointProb)
			matrix_condJointProb.append(temp_list_condJointProb)
			matrix_jointProb.append(temp_list_jointProb)
		    conditional_jointprob[classes[k]][attr_1][attr_2] = matrix_condJointProb
		    jointProb[classes[k]][attr_1][attr_2] = matrix_jointProb




def calculate_InformationGain(data, meta) :
    for attr_1 in meta.names()[:-1] :
        for attr_2 in meta.names()[:-1] :
	    if (attr_1 == attr_2) :
		continue
	    else :
		sum = 0
		for attr_1_val in attributes[attr_1] :
		    #print 'Value attr 1 is'
                    #print attr_1_val
		    for attr_2_val in attributes[attr_2] :
			for k in range(len(classes)) :
			    numerator = jointProb[classes[k]][attr_1][attr_2][(attributes[attr_1].index(attr_1_val))][(attributes[attr_2].index(attr_2_val))] * math.log((conditional_jointprob[classes[k]][attr_1][attr_2][(attributes[attr_1].index(attr_1_val))][(attributes[attr_2].index(attr_2_val))] / (conditional_prob[classes[k]][attr_1][attr_1_val] * conditional_prob[classes[k]][attr_2][attr_2_val])), 2)
			    sum += numerator
		CMI[attr_1][attr_2] = sum
		sum = 0





def isNotEqual (vector1, vector2) :
    vector1.sort()
    vector2.sort()
    if (vector1 == vector2) :
	return False
    else :
	return True




def primAlgo(data , meta) :
    V = []
    V = meta.names()[:-1]
    #V_new = []
    #E_new = []

    first_feature = meta.names()[0]
    V_new.append(first_feature)

    while(isNotEqual(V, V_new)) :
        max_weight = {}
        myMaxWeight = -1
        chosenVertex = []
        chosenEdge = {}
        
	for vertex_new in V_new :
            max_weight[vertex_new] = {}
            for vertex in V :
                if vertex in V_new :
                    max_weight[vertex_new][vertex] = -24
                else :
                    max_weight[vertex_new][vertex] = CMI[vertex_new][vertex]
        
	candidateList = {}
        for vnew in max_weight.keys() :
            myMaxRowWeight = max_weight[vnew][max_weight[vnew].keys()[0]]
            candidateList[vnew] = []
            selected_vold = max_weight[vnew].keys()[0]
	    candidateList[vnew].append(selected_vold)
	    candidateList[vnew].append(myMaxRowWeight)
            for vold in max_weight[vnew].keys()[1:] :
                if (myMaxRowWeight == max_weight[vnew][vold]) :
                    if(meta.names()[:-1].index(vold) < meta.names()[:-1].index(selected_vold)) :
                        candidateList[vnew] = []
                        candidateList[vnew].append(vnew)
                        candidateList[vnew].append(myMaxRowWeight)
                elif (myMaxRowWeight < max_weight[vnew][vold]) :
                    candidateList[vnew] = []
                    candidateList[vnew].append(vold)
                    candidateList[vnew].append(max_weight[vnew][vold])
                    myMaxRowWeight = max_weight[vnew][vold]

        counter = 0
        myMaxWeightInColumn = candidateList[candidateList.keys()[0]][-1]
        selectedVold = candidateList[candidateList.keys()[0]][0]
        selectedVnew = candidateList.keys()[0]
        for vnew in candidateList.keys() :
            if(myMaxWeightInColumn == candidateList[vnew][-1]) :
                if(meta.names()[:-1].index(selectedVold) == meta.names()[:-1].index(candidateList[vnew][0])) :
                    if(meta.names()[:-1].index(vnew) <  meta.names()[:-1].index(selectedVnew)) :
                        selectedVnew = vnew
                        #myMaxWeightInColumn = candidateList[vold][-1]
                elif(meta.names()[:-1].index(candidateList[vnew][0]) < meta.names()[:-1].index(selectedVold)) :
                    selectedVnew = vnew
                    selectedVold = candidateList[vnew][0]
            elif(myMaxWeightInColumn < candidateList[vnew][-1]) :
                selectedVold = candidateList[vnew][0]
                selectedVnew = vnew
                myMaxWeightInColumn = candidateList[vnew][-1]

	V_new.append(selectedVold)
        E_new.append([selectedVnew, selectedVold])




def trim_data(attr, parent_val, class_val, data) :
    returnData = []
    for instance in data :
	if(instance[attributes_index[attr]] == parent_val and instance[-1] == class_val) :
	    returnData.append(instance)
    return returnData




def calculateCPT(data, meta) :
    #print attributes
    #print E_new
    vertex_covered = []
    for k in range(len(classes)) :
	CPT[classes[k]] = {}
	for edge in E_new :
	    #print 'My edge is'	    
	    #print edge
	    vertex_covered.append(edge[-1])
	    #e[-1] Child
	    #e[0] Parent
	    if(edge[0] not in CPT[classes[k]].keys()) :
	    	CPT[classes[k]][edge[0]] = {}
	    CPT[classes[k]][edge[0]][edge[-1]] = {}
	    for parent_value in attributes[edge[0]] :
		CPT[classes[k]][edge[0]][edge[-1]][parent_value] = {}
		for child_value in attributes[edge[-1]] :
		    count = 0
		    trimmed_data = trim_data(edge[0], parent_value, classes[k], data)
		    for instance in trimmed_data :
			if(instance[attributes_index[edge[-1]]] == child_value) :
			    count+=1
		    numerator = count + 1
		    denominator = len(trimmed_data) + len(attributes[edge[-1]])
		    CPT[classes[k]][edge[0]][edge[-1]][parent_value][child_value] = numerator / denominator
    #print CPT
    missing = list(set(meta.names()[:-1]) - set(vertex_covered))
    #print missing
    root.append(missing[0])
    CPT[classes[0]]['root'] = {}
    CPT[classes[1]]['root'] = {}
    for value in attributes[missing[0]] :
        CPT[classes[0]]['root'][value] = conditional_prob[classes[0]][missing[0]][value]
	CPT[classes[1]]['root'][value] = conditional_prob[classes[1]][missing[0]][value]
    #print CPT




def calculate_CMI(data, meta) :
    calculate_requiredProb(data, meta)
    calculate_InformationGain(data, meta)




def naive_bayes(test_data, test_meta) :
    correct_classification = 0
    for feature in test_meta.names()[:-1] :
        print feature + ' class'
    print
    multiplication = {}
    for i in range(len(test_data)) :
	test_instance = test_data[i]
	for j in range(len(classes)) :
	    multiplication[classes[j]] = 1
	    for attr in test_meta.names()[:-1] :
		multiplication[classes[j]] *= conditional_prob[classes[j]][attr][test_instance[attributes_index[attr]]]
	
	denominator = class_prob[classes[0]] * multiplication[classes[0]] + class_prob[classes[1]] * multiplication[classes[1]]
	
	#Binary Classification
	if (class_prob[classes[0]] * multiplication[classes[0]] > class_prob[classes[1]] * multiplication[classes[1]]) :
		print classes[0], test_instance[-1], round((class_prob[classes[0]] * multiplication[classes[0]])/denominator, 12)
		if(classes[0] == test_instance[-1]) :
		    correct_classification += 1
	else :
		print classes[1], test_instance[-1], round((class_prob[classes[1]] * multiplication[classes[1]])/denominator, 12)
		if(classes[1] == test_instance[-1]) :
                    correct_classification += 1
    print correct_classification
    return correct_classification




def calculate(attr_value, index, class_val, test_instance) :
    #print root
    myAttr = attr_value
    for attr in attributes_index.keys() :
	if (attributes_index[attr] == index) :
		myAttr = attr
    #print myAttr
    if(myAttr == root[0]) :
	#print 'in'
	return CPT[class_val]['root'][attr_value]
    else :
	#returnVal = 1
	for edge in E_new :
	    if (edge[-1] == myAttr) :
		#print test_instance[attributes_index[edge[0]]]
		#print attr_value
		return CPT[class_val][edge[0]][edge[-1]][test_instance[attributes_index[edge[0]]]][attr_value]
	#return returnVal
    return 0	




def tan(test_data, test_meta) :
    correct_classification = 0
    print root[0], 'class'
    for attribute in test_meta.names()[:-1]:
        for edge in E_new :
	    if(attribute == edge[-1]):
		print edge[-1], edge[0], 'class'
	        break
    print
    multiplication = {}
    for i in range(len(test_data)) :
        test_instance = test_data[i]
	#print test_instance
        for j in range(len(classes)) :
            multiplication[classes[j]] = 1
	    for k in range(len(test_instance) - 1) :
		returnValue = calculate(test_instance[k], k, classes[j], test_instance)
		multiplication[classes[j]] *= returnValue
	#Binary Classification
	denominator = class_prob[classes[0]] * multiplication[classes[0]] + class_prob[classes[1]] * multiplication[classes[1]]
        if (class_prob[classes[0]] * multiplication[classes[0]] > class_prob[classes[1]] * multiplication[classes[1]]) :
                print classes[0],test_instance[-1], round((class_prob[classes[0]] * multiplication[classes[0]]) / denominator, 12)
		if(classes[0] == test_instance[-1]) :
                    correct_classification += 1
        else :
                print classes[1], test_instance[-1], round((class_prob[classes[1]] * multiplication[classes[1]]) / denominator, 12)
		if(classes[1] == test_instance[-1]) :
                    correct_classification += 1
    print correct_classification
    return correct_classification




def part2_naive_bayes(data, meta, test_data, test_meta) :
    conditional_prob = {}
    class_prob = {}
    separate_data = {}
    classes = []
    attributes = {}
    attributes_index = {}
    laplace = 1
    different_sizes = [25, 50, 100]
    accuracy = {}
    reps = 0
    while reps < 4 :
#	reps += 1
	conditional_prob = {}
    	class_prob = {}
    	separate_data = {}
    	classes = []
    	attributes = {}
    	attributes_index = {}
    	laplace = 1
	accuracy[reps] = {}
    	different_sizes = [25, 50, 100]
	#y_axis = []
        for i in different_sizes :
	    accuracy[reps][i] = []
	    trainset = []
	    generatedIndices = []
	    while (len(trainset) != i) :
	        index = randint(0, i-1)
	        if index not in generatedIndices :
		    trainset.append(data[index])
		    generatedIndices.append(index)
	    initialize(trainset, meta)
    	    calculate_conditional_prob(trainset, meta)
	    accuracy_temp = naive_bayes(test_data, test_meta)
	    accuracy[reps][i] = round((accuracy_temp / 42), 2) * 100
	reps += 1
    y_axis = [(accuracy[0][25] + accuracy[1][25] + accuracy[2][25] + accuracy[3][25]) / 4, (accuracy[0][50] + accuracy[1][50] + accuracy[2][50] + accuracy[3][50]) / 4, (accuracy[0][100] + accuracy[1][100] + accuracy[2][100] + accuracy[3][100]) / 4]
    plt.figure()
    plt.plot(different_sizes, y_axis, label="Avg Accuracy vs Size for Naive Bayes", marker='H')
    plt.xlabel("Training set size")
    plt.ylabel("Test set accuracy (%)")
    plt.title("Test accuracy vs Training set size")
    plt.xlim(0, 101)
    plt.ylim(0, 100)
    plt.grid(True)
    plt.legend(loc="lower right")
    plt.savefig("graphs/accuracy_vs_size_naive_bayes.png") 



def part2_tan(data, meta, test_data, test_meta) :
    conditional_prob = {}
    class_prob = {}
    separate_data = {}
    classes = []
    attributes = {}
    attributes_index = {}
    laplace = 1
    different_sizes = [25, 50, 100]
    accuracy = {}
    reps = 0
    #For TAN
    CMI = {}
    conditional_jointprob = {}
    jointProb = {}
    V_new = []
    E_new = []
    CPT = {}
    root = []

    while reps < 4 :
        conditional_prob = {}
        class_prob = {}
        separate_data = {}
        classes = []
        attributes = {}
        attributes_index = {}
        laplace = 1
        accuracy[reps] = {}
        different_sizes = [25, 25, 25]
	#For TAN
	CMI = {}
	conditional_jointprob = {}
	jointProb = {}
	V_new = []
	E_new = []
	CPT = {}
	root = []

        for i in different_sizes :
            accuracy[reps][i] = []
            trainset = []
            generatedIndices = []
            while (len(trainset) != i) :
                index = randint(0, i-1)
                if index not in generatedIndices :
                    trainset.append(data[index])
                    generatedIndices.append(index)
            initialize(trainset, meta)
            calculate_conditional_prob(trainset, meta)
	    calculate_CMI(trainset, meta)
            primAlgo(trainset, meta)
            calculateCPT(trainset, meta)
            accuracy_temp = tan(test_data, test_meta)
            accuracy[reps][i] = round((accuracy_temp / 42), 2) * 100
        reps += 1
    y_axis = [(accuracy[0][25] + accuracy[1][25] + accuracy[2][25] + accuracy[3][25]) / 4, (accuracy[0][50] + accuracy[1][50] + accuracy[2][50] + accuracy[3][50]) / 4, (accuracy[0][100] + accuracy[1][100] + accuracy[2][100] + accuracy[3][100]) / 4]
    plt.figure()
    plt.plot(different_sizes, y_axis, label="Avg Accuracy vs Size for TAN", marker='H')
    plt.xlabel("Training set size")
    plt.ylabel("Test set accuracy (%)")
    plt.title("Test accuracy vs Training set size")
    plt.xlim(0, 101)
    plt.ylim(0, 100)
    plt.grid(True)
    plt.legend(loc="lower right")
    plt.savefig("graphs/accuracy_vs_size_tan.png")




def main(arg) :
    data, meta = read_arff(arg[0])
    initialize(data, meta)
    calculate_conditional_prob(data, meta)
    test_data, test_meta = read_arff(arg[1])
    
    if(arg[2] == 'n') :
	naive_bayes(test_data, test_meta)
	#part2_naive_bayes(data, meta, test_data, test_meta)
    else :
	calculate_CMI(data, meta)
	primAlgo(data, meta)
	calculateCPT(data, meta)
	tan(test_data, test_meta)
	#part2_tan(data, meta, test_data, test_meta)



main(sys.argv[1:])
