#%%
import time
import keras_cv
from tensorflow import keras
import matplotlib.pyplot as plt


# Based on
# https://keras.io/guides/keras_cv/generate_images_with_stable_diffusion/
# https://keras.io/examples/generative/finetune_stable_diffusion/

#%%
keras.mixed_precision.set_global_policy("mixed_float16")

model = keras_cv.models.StableDiffusion(img_width=512, img_height=512, jit_compile=True)


#%%
promt = "The hand-written digit three"
negativePromt = "color"
images = model.text_to_image(promt, negative_prompt=negativePromt, batch_size=3)


def plot_images(images):
    plt.figure(figsize=(20, 20))
    for i in range(len(images)):
        ax = plt.subplot(1, len(images), i + 1)
        plt.imshow(images[i])
        plt.axis("off")


plot_images(images)

#%%
fileName = "-".join(promt.split(" "))
for i, image in enumerate(images):
    keras.utils.save_img(f"{fileName}_{i}.png", image)
# %%
