import matplotlib.pyplot as plt
import numpy as np


l = []

f = open('output5.txt', 'r')
for line in f:
    l.append(line.split()[2:4])

print l
l.sort(key=lambda x: float(x[1]), reverse = True)

print 'hello'
print l

myY = []
myScore = []
count_tpr = 0
count_fpr = 0
for i in range(len(l)) :
    if l[i][0] == 'Rock':
	myY.append(0)
	count_fpr = count_fpr + 1
    else :
	myY.append(1)
	count_tpr = count_tpr + 1
    myScore.append(float(l[i][1]))


#score = np.array([0.9, 0.8, 0.7, 0.6, 0.55, 0.54, 0.53, 0.52, 0.51, 0.505, 0.4, 0.39, 0.38, 0.37, 0.36, 0.35, 0.34, 0.33, 0.30, 0.1])
#y = np.array([1,1,0, 1, 1, 1, 0, 0, 1, 0, 1,0, 1, 0, 0, 0, 1 , 0, 1, 0])

score = np.array(myScore)
y = np.array(myY)

print score
print y
roc_x = []
roc_y = []
current = 0
currentClass = myY[0]
while current < len(myScore):
    TPR = 0
    FPR = 0
    Tp = 0
    Fp = 0
    r_x = 0
    r_y = 0
    for i in range(current) :
	if(myY[i] == 1):
	    Tp += 1
	else :
	    Fp += 1
    print Tp
    r_y = Tp / float(count_tpr)
    r_x = Fp / float(count_fpr)
    roc_x.append(r_x)
    roc_y.append(r_y)
    
    i = current
    while current < len(myScore) :
	if(myY[i] == currentClass) :
	    current = current + 1
	    i = i + 1
	else:
	    break
    if current < len(myScore):
    	currentClass = myY[current]
    else:
	currentClass = myY[-1]
    print current
print roc_x
print roc_y





#min_score = min(score)
#max_score = max(score)
#thr = np.linspace(min_score, max_score, 100)
#FP=0
#TP=0
#N = sum(y)
#P = len(y) - N

#for (i, T) in enumerate(thr):
#    for i in range(0, len(score)):
#        if (score[i] > T):
#            if (y[i]==1):
#                TP = TP + 1
#            if (y[i]==0):
#                FP = FP + 1
#    roc_x.append(FP/float(N))
#    roc_y.append(TP/float(P))
#    FP=0
#    TP=0

plt.xlabel("FPR")
plt.ylabel("TPR")
plt.title("ROC Curve")
plt.scatter(roc_x, roc_y)
plt.grid(True)

#plt.show()
plt.savefig("roc.png")
