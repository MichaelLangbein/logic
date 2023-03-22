
# Title: Image segmentation with a U-Net-like architecture
# Author: [fchollet](https://twitter.com/fchollet)
# Date created: 2019/03/20
# Last modified: 2020/04/20
# Description: Image segmentation model trained from scratch on the Oxford Pets dataset.
# Accelerator: GPU


#%% Download the data


# shell
# curl -O https://thor.robots.ox.ac.uk/~vgg/data/pets/images.tar.gz
# curl -O https://thor.robots.ox.ac.uk/~vgg/data/pets/annotations.tar.gz
# tar -xf images.tar.gz
# tar -xf annotations.tar.gz



#%% Prepare paths of input images and target segmentation masks


#%%

import os

input_dir = "data/images/"
target_dir = "data/annotations/trimaps/"
img_size = (160, 160)
num_classes = 3
batch_size = 32

input_img_paths = sorted(
    [
        os.path.join(input_dir, fname)
        for fname in os.listdir(input_dir)
        if fname.endswith(".jpg")
    ]
)
target_img_paths = sorted(
    [
        os.path.join(target_dir, fname)
        for fname in os.listdir(target_dir)
        if fname.endswith(".png") and not fname.startswith(".")
    ]
)

print("Number of samples:", len(input_img_paths))

for input_path, target_path in zip(input_img_paths[:10], target_img_paths[:10]):
    print(input_path, "|", target_path)




#%% Prepare `Sequence` class to load & vectorize batches of data


from tensorflow import keras
import numpy as np
from tensorflow.keras.preprocessing.image import load_img


class OxfordPets(keras.utils.Sequence):
    # Helper to iterate over the data (as Numpy arrays).

    def __init__(self, batch_size, img_size, input_img_paths, target_img_paths):
        self.batch_size = batch_size
        self.img_size = img_size
        self.input_img_paths = input_img_paths
        self.target_img_paths = target_img_paths

    def __len__(self):
        return len(self.target_img_paths) // self.batch_size

    def __getitem__(self, idx):
        # Returns tuple (input, target) correspond to batch #idx.
        i = idx * self.batch_size
        batch_input_img_paths = self.input_img_paths[i : i + self.batch_size]
        batch_target_img_paths = self.target_img_paths[i : i + self.batch_size]
        x = np.zeros((self.batch_size,) + self.img_size + (3,), dtype="float32")
        for j, path in enumerate(batch_input_img_paths):
            img = load_img(path, target_size=self.img_size)
            x[j] = img
        y = np.zeros((self.batch_size,) + self.img_size + (1,), dtype="uint8")
        for j, path in enumerate(batch_target_img_paths):
            img = load_img(path, target_size=self.img_size, color_mode="grayscale")
            y[j] = np.expand_dims(img, 2)
            # Ground truth labels are 1, 2, 3. Subtract one to make them 0, 1, 2:
            y[j] -= 1
        return x, y



#%% Prepare U-Net Xception-style model
from unet import make_unet, make_mini_unet


# Free up RAM in case the model definition cells were run multiple times
keras.backend.clear_session()

# Build model
model = make_mini_unet(img_size[0], img_size[1], 3, num_classes)
model.summary()


#%% Set aside a validation split


import random

# Split our img paths into a training and a validation set
val_samples = 1000
random.Random(1337).shuffle(input_img_paths)
random.Random(1337).shuffle(target_img_paths)
train_input_img_paths = input_img_paths[:-val_samples]
train_target_img_paths = target_img_paths[:-val_samples]
val_input_img_paths = input_img_paths[-val_samples:]
val_target_img_paths = target_img_paths[-val_samples:]

# Instantiate data Sequences for each split
train_gen = OxfordPets(batch_size, img_size, train_input_img_paths, train_target_img_paths)
val_gen = OxfordPets(batch_size, img_size, val_input_img_paths, val_target_img_paths)


#%% Train the model


# Configure the model for training.
# We use the "sparse" version of categorical_crossentropy
# because our target data is integers.
model.compile(optimizer="rmsprop", loss="sparse_categorical_crossentropy")

callbacks = [
    keras.callbacks.ModelCheckpoint("oxford_segmentation.h5", save_best_only=True)
]

# Train the model, doing validation at the end of each epoch.
epochs = 15
model.fit(train_gen, epochs=epochs, validation_data=val_gen, callbacks=callbacks)


#%% Visualize predictions


# Generate predictions for all images in the validation set

val_gen = OxfordPets(batch_size, img_size, val_input_img_paths, val_target_img_paths)
val_preds = model.predict(val_gen)

#%%
import matplotlib.pyplot as plt


def display(indx):
    batchNr = indx // batch_size
    batchIndx = indx % batch_size
    inputs, targets = val_gen.__getitem__(batchNr)
    input = inputs[batchIndx]
    target = targets[batchIndx]
    pred = val_preds[indx]
    fig, axes = plt.subplots(1, 3)
    axes[0].imshow(np.array(input, dtype=np.int16))
    axes[1].imshow(target, cmap="gray")
    axes[2].imshow(pred, cmap="gray")

#%%
display(14)
# %%
