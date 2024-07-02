#%%
import numpy as np
import matplotlib.pyplot as plt

def sigmoid(x):
    return 1 / (1 + np.exp(-x))

def soft_xor(a, b):
    # return sigmoid(a - b)
    sum = a + b
    diff = np.abs(sum - 1.)
    return np.abs(sum - 1)


x = np.arange(0.0, 1.0, 0.1)
y = np.arange(0.0, 1.0, 0.1)
X,Y = np.meshgrid(x, y) # grid of point
Z = soft_xor(X, Y) # evaluation of the function on the grid

im = plt.imshow(Z) # drawing the function
plt.show()

# %%
