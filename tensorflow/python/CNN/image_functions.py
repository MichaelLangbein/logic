# -*- coding: utf-8 -*-
import os
from random import choice, sample

import numpy as np
from skimage.io import imread
from skimage.transform import rotate
from tensorflow.keras.utils import to_categorical


def preprocessing_image_rgb(x):
    # define mean and std values
    mean = [np.mean(x[:, :, 0]), np.mean(x[:, :, 1]), np.mean(x[:, :, 2])]
    std = [np.std(x[:, :, 0]), np.std(x[:, :, 1]), np.std(x[:, :, 2])]
    # loop over image channels
    for idx, mean_value in enumerate(mean):
        x[..., idx] -= mean_value
        x[..., idx] /= std[idx]
    return x


def preprocessing_image_ms(x):
    # define mean and std values
    mean = x.mean(axis=(0,1))
    std = x.std(axis=(0,1))
    # loop over image channels
    for idx, mean_value in enumerate(mean):
        x[..., idx] -= mean_value
        if np.isnan(std[idx]):
            continue
        x[..., idx] /= std[idx]
    return x


def categorical_label_from_full_file_name(files, class_indices):
    # file basename without extension
    base_name = [os.path.splitext(os.path.basename(i))[0] for i in files]
    # class label from filename
    base_name = [i.split("_")[0] for i in base_name]
    # label to indices
    image_class = [class_indices[i] for i in base_name]
    # class indices to one-hot-label
    return to_categorical(image_class, num_classes=len(class_indices))


def simple_image_generator(files, class_indices, batch_size=32,
                           rotation_range=0, horizontal_flip=False,
                           vertical_flip=False):

    while True:
        # select batch_size number of samples without replacement
        batch_files = sample(files, batch_size)
        # get one_hot_label
        batch_Y = categorical_label_from_full_file_name(batch_files,
                                                        class_indices)
        # array for images
        batch_X = []
        # loop over images of the current batch
        for idx, input_path in enumerate(batch_files):
            image = np.array(imread(input_path), dtype=float)
            image = preprocessing_image_ms(image)
            # process image
            if horizontal_flip:
                # randomly flip image up/down
                if choice([True, False]):
                    image = np.flipud(image)
            if vertical_flip:
                # randomly flip image left/right
                if choice([True, False]):
                    image = np.fliplr(image)
            # rotate image by random angle between
            # -rotation_range <= angle < rotation_range
            if rotation_range is not 0:
                angle = np.random.uniform(low=-abs(rotation_range),
                                          high=abs(rotation_range))
                image = rotate(image, angle, mode='reflect',
                               order=1, preserve_range=True)
            # put all together
            batch_X += [image]
        # convert lists to np.array
        X = np.array(batch_X)
        Y = np.array(batch_Y)

        yield(X, Y)
