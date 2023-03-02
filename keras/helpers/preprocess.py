#%%
from PIL import Image
import os

# Files can be downloaded with google-chrome's image downloader plugin

# %%
imagePath = os.path.join(os.getcwd(), 'downloads')
targetPath = os.path.join(os.getcwd(), 'preprocessed')

for i, fileName in enumerate(os.listdir(imagePath)):

    fullImagePath = os.path.join(imagePath, fileName)
    fullTargetPath = os.path.join(targetPath, f"image_{i}.jpg")

    print(f"Editing image {fullImagePath}")

    image = Image.open(fullImagePath)
    imageRgb = image.convert('RGB')
    imageResized = imageRgb.resize((64, 64))
    with open(fullTargetPath, "wb") as f:
        imageResized.save(f)


# %%
