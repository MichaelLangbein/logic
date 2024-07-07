import os
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.models import load_model



from image_functions import preprocessing_image_rgb


path_to_split_datasets = "./data"

path_to_home = os.path.expanduser("~")
path_to_split_datasets = path_to_split_datasets.replace("~", path_to_home)
path_to_validation = os.path.join(path_to_split_datasets, "validation")

test_datagen = ImageDataGenerator(
    preprocessing_function=preprocessing_image_rgb)

validation_generator = test_datagen.flow_from_directory(
    path_to_validation,
    target_size=(64, 64),
    batch_size=32,
    class_mode='categorical')


model = load_model("path/to/model.hdf5")
