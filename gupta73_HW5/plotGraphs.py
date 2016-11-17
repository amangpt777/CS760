#!/usr/bin/env

import matplotlib.pyplot as plt 

y_axis = [(158.0/208.0)*100, (155.0/208.0)*100, (155.0/208.0)*100, (155.0/208.0)*100]
different_sizes = [25, 50, 75, 100]
plt.figure()
plt.plot(different_sizes, y_axis, label="Accuracy vs Epoch", marker='H')
plt.xlabel("Epoch")
plt.ylabel("Accuracy (%)")
plt.title("Test accuracy vs Epoch")
plt.xlim(0, 101)
plt.ylim(0, 150)
plt.grid(True)
plt.legend(loc="lower right")
plt.savefig("AccuracyWithEpoch.png")
