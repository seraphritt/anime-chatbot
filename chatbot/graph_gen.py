import matplotlib.pyplot as plt
import numpy as np

time = np.array([3.05668, 1.70986,  1.00894, 0.68219])
epochs = np.array([400, 200, 100, 50])
plt.figure(figsize=(10, 6), dpi=100)
plt.scatter(time, epochs)
plt.plot(time, epochs)
plt.xlabel("Tempo (s)")
plt.ylabel("Épocas")
plt.savefig("graph_epochsxtime.png")
plt.show()
