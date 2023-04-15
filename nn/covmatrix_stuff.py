#%%
import numpy as np
import matplotlib.pyplot as plt


#%%
    # sports food romance art
A = np.array([
    [3, 1, 2, 0], # Andy
    [3, 3, 0, 0], # Benny
    [2, 0, 1, 3], # Chloe
    [3, 2, 1, 0], # Danny
    [2, 1, 2, 3], # Eva
    [0, 2, 2, 1]  # Fiona
])

#%%
def distance(a, b):
    return np.sqrt(np.sum((a-b)**2))

def distanceMatrix(X):
    P, H = X.shape
    D = np.zeros((P, P))
    for p1 in range(P):
        for p2 in range(P):
            D[p1, p2] = distance(X[p1], X[p2])
    return D

#%% Self-attention
distance0 = distanceMatrix(A)
plt.imshow(distance0)

#%% subtract mean
X1 = (A.T - np.mean(A, 1)).T
HobbyCovar = X1.T @ X1
Y1 = X1 @ HobbyCovar

distance1 = distanceMatrix(Y1)
plt.imshow(distance1)


# %% PCA

X2 = A - np.mean(A, 0)
PersonCovar = X2 @ X2.T

evals, evecs = np.linalg.eigh(PersonCovar)
Y2 = evecs @ X2

distance2 = distanceMatrix(Y2)
plt.imshow(distance2)
# %%
