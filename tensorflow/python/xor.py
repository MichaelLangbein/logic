#%%
import keras as k
from keras.models import Sequential
from keras.layers import Dense, Dropout, Activation
from keras.optimizers import SGD
import numpy as np 

X = np.array([[0,0],[0,1],[1,0],[1,1]])
y = np.array([[0],[1],[1],[0]])

model = k.Sequential([
        k.layers.Dense(4, activation='tanh', input_shape=(2,)),
        k.layers.Dense(4, activation='tanh'),
        k.layers.Dense(1, activation='sigmoid'),
])

model.compile(
    loss='binary_crossentropy', 
    optimizer="sgd",
    metrics=['accuracy']
)


# %%
model.fit(X, y, epochs=500, batch_size=1)
print(model.predict(X))
# %%
