#%%
import keras as k
from dataLoader import OxfordPets, input_img_paths, target_img_paths
from unet import make_unet
import random

# %%
k.backend.clear_session()


# %%
num_classes = 3
batch_size = 32
w, h, d = 160, 160, 3


# %%
model = make_unet(w, h, d, num_classes)

# %%
val_samples = 1000
random.Random().shuffle(input_img_paths)
random.Random().shuffle(target_img_paths)
train_input_img_paths = input_img_paths[:-val_samples]
train_target_img_paths = target_img_paths[:-val_samples]
val_input_img_paths = input_img_paths[-val_samples:]
val_target_img_paths = target_img_paths[-val_samples:]

train_gen = OxfordPets(batch_size, (w, h), train_input_img_paths, train_target_img_paths)
val_gen = OxfordPets(batch_size, (w, h), val_input_img_paths, val_target_img_paths)

# %%
model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy")
callbacks = [
    k.callbacks.ModelCheckpoint("oxford_segmentation.h5", save_best_only=True)
]
epochs = 15
model.fit(train_gen, epochs=epochs, validation_data=val_gen, callbacks=callbacks)


# %%
val_pred = model.predict(val_gen)


#%%
import matplotlib.pyplot as plt


def display(indx):
    batchNr = indx // batch_size
    batchIndx = indx % batch_size
    inputs, targets = val_gen.__getitem__(batchNr)
    input = inputs[batchIndx]
    target = targets[batchIndx]
    pred = val_pred[indx]
    fig, axes = plt.subplots(1, 3)
    axes[0].imshow(input)
    axes[1].imshow(target)
    axes[2].imshow(pred)

#%%
display(10)