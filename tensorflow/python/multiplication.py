#%%
import numpy as np
import matplotlib.pyplot as plt
import keras as k

#%% 


# %%

# a simple neural network made of 4 dense layers
# must use relu instead of sigmoid to work properly

model = k.Sequential([
    k.layers.Dense(64, activation='relu', input_shape=(2,)),
    k.layers.Dense(64, activation='relu'),
    k.layers.Dense(64, activation='relu'),
    k.layers.Dense(1, activation='relu'),
])
model.compile(optimizer=k.optimizers.Adagrad(),
              loss=k.losses.MeanSquaredError(),
              metrics=['accuracy'] # actually, accuracy will always be 0 in regression tasks
)


# %% training

# nn only works properly on numbers smaller than 1.0
x_train = np.random.random((100_000, 2))
y_train = x_train[:, 0] * x_train[:, 1]

model.fit(x_train, y_train, epochs=10, batch_size=32)


model.predict(np.array([[0.8, 0.5], [0.8, 0.1], [0.2, 0.2]]))


# %% saving for use in browser
import tensorflowjs as tfjs
tfjs.converters.save_keras_model(model, "./savedModels/multiplier")

# %% 
