#!/usr/bin/env

import matplotlib.pyplot as plt 

y_axis = [(147.0/208.0)*100, (156.0/208.0)*100, (170.0/208.0)*100, (167.0/208.0)*100, (173.0/208.0)*100]
different_sizes = [5, 10, 15, 20, 25]
plt.figure()
plt.plot(different_sizes, y_axis, label="Accuracy vs Folds", marker='H')
plt.xlabel("Number of Folds")
plt.ylabel("Accuracy (%)")
plt.title("Test accuracy vs Epoch")
plt.xlim(0, 30)
plt.ylim(0, 101)
plt.grid(True)
plt.legend(loc="lower right")
plt.savefig("AccuracyWithFold.png")
