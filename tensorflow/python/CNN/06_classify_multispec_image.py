#%%
#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Code for the PyCon.DE 2018 talk by Jens Leitloff and Felix M. Riese.

PyCon 2018 talk: Satellite data is for everyone: insights into modern remote
sensing research with open data and Python.

License: MIT

"""
import os
from osgeo import gdal
import numpy as np
from skimage.io import imread
# from skimage.util import pad
from tensorflow.keras.models import load_model
from tqdm import tqdm



#%%
# input files
path_to_image = "./verification_multi/"
path_to_model = "./models/input/convertme_time_acc0.925.h5"
# output files
path_to_label_image = "./verification/_10m_vgg_ms_label.tif"
path_to_prob_image = "./verification/_10m_vgg_ms_prob.tif"

#%%
image1 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b1.tiff"), dtype=float)
image2 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b2.tiff"), dtype=float)
image3 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b3.tiff"), dtype=float)
image4 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b4.tiff"), dtype=float)
image5 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b5.tiff"), dtype=float)
image6 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b6.tiff"), dtype=float)
image7 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b7.tiff"), dtype=float)
image8 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b8.tiff"), dtype=float)
image8a = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b8a.tiff"), dtype=float)
image9 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b9.tiff"), dtype=float)
image10 = np.zeros(image9.shape)
image11 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b11.tiff"), dtype=float)
image12 = np.array(imread("/home/michael/Desktop/code/logic/tensorflow/python/CNN/verification_multi/b12.tiff"), dtype=float)
image = np.stack([image1, image2, image3, image4, image5, image6, image7, image8, image8a, image9, image10, image11, image12], axis=2)
image_orig = image

#%%

# read image and model
# image = np.array(imread(path_to_image), dtype=float)
_, num_cols_unpadded, _ = image.shape
model = load_model(path_to_model)
# get input shape of model
_, input_rows, input_cols, input_channels = model.layers[0].input_shape[0]
_, output_classes = model.layers[-1].output_shape
in_rows_half = int(input_rows/2)
in_cols_half = int(input_cols/2)

# import correct preprocessing
if input_channels == 3:
    from image_functions import preprocessing_image_rgb as preprocessing_image
else:
    from image_functions import preprocessing_image_ms as preprocessing_image

#%%
# pad image
image = np.pad(image, (
        (input_rows, input_rows),
        (input_cols, input_cols),
        (0, 0),
    ), 'symmetric')

# don't forget to preprocess
mean = image.mean(axis=(0,1))
std = image.std(axis=(0,1))
image = preprocessing_image(image, mean, std)
num_rows, num_cols, _ = image.shape

#%%
# sliding window over image
image_classified_prob = np.zeros((num_rows, num_cols, output_classes))
row_images = np.zeros((num_cols_unpadded, input_rows,
                       input_cols, input_channels))
for row in tqdm(range(input_rows, num_rows-input_rows), desc="Processing..."):
    # get all images along one row
    for idx, col in enumerate(range(input_cols, num_cols-input_cols)):
        # cut smal image patch
        row_images[idx, ...] = image[row-in_rows_half:row+in_rows_half,
                                     col-in_cols_half:col+in_cols_half, :]
    # classify images
    row_classified = model.predict(row_images, batch_size=1024, verbose=0)
    # put them to final image
    image_classified_prob[row, input_cols:num_cols-input_cols, : ] = row_classified

# crop padded final image
image_classified_prob = image_classified_prob[input_rows:num_rows-input_rows,
                                              input_cols:num_cols-input_cols, :]
image_classified_label = np.argmax(image_classified_prob, axis=-1)
image_classified_prob = np.sort(image_classified_prob, axis=-1)[..., -1]



#%%
import matplotlib.pyplot as plt

# plt.imshow(image, cmap='gray', interpolation='none')
# plt.imshow(image_classified_label, cmap='jet', alpha=0.25, interpolation='none')

def toRgbSimple(c):
    if c == 0: # AnnualCrop 
        return [0, 255, 255]
    if c == 1: # Forest 
        return [0, 255, 0]
    if c == 2: # HerbaceousVegetation 
        return [0, 125, 0]
    if c == 3: # Highway 
        return [30, 30, 30]
    if c == 4: # Industrial 
        return [100, 30, 30]
    if c == 5: # Pasture 
        return [0, 125, 0]
    if c == 6: # PermanentCrop 
        return [0, 125, 125]
    if c == 7: # Residential 
        return [100, 100, 100]
    if c == 8: # River 
        return [0, 0, 255]
    if c == 9: # SeaLake
        return [0, 0, 255]




rows, cols = image_classified_label.shape
image_classified_label_rgb = np.zeros([rows, cols, 3], dtype=np.uint8)
for i in range(rows):
    for j in range(cols):
        image_classified_label_rgb[i, j] = toRgbSimple(image_classified_label[i, j])


fig, axes = plt.subplots(1, 2)
img0 = axes[0].imshow(image_orig[:, :, [6, 7, 8]],  interpolation='none')
img1 = axes[1].imshow(image_classified_label_rgb / 255, interpolation='none')




#%%
# write image as Geotiff for correct georeferencing
# read geotransformation
image = gdal.Open(path_to_image, gdal.GA_ReadOnly)
geotransform = image.GetGeoTransform()

# create image driver
driver = gdal.GetDriverByName('GTiff')
# create destination for label file
file = driver.Create(path_to_label_image,
                     image_classified_label.shape[1],
                     image_classified_label.shape[0],
                     1,
                     gdal.GDT_Byte,
                     ['TFW=YES', 'NUM_THREADS=1'])
file.SetGeoTransform(geotransform)
file.SetProjection(image.GetProjection())
# write label file
file.GetRasterBand(1).WriteArray(image_classified_label)
file = None
# create destination for probability file
file = driver.Create(path_to_prob_image,
                     image_classified_prob.shape[1],
                     image_classified_prob.shape[0],
                     1,
                     gdal.GDT_Float32,
                     ['TFW=YES', 'NUM_THREADS=1'])
file.SetGeoTransform(geotransform)
file.SetProjection(image.GetProjection())
# write label file
file.GetRasterBand(1).WriteArray(image_classified_prob)

# %%
