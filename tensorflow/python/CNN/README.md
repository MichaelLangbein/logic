[![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.3268451.svg)](https://doi.org/10.5281/zenodo.3268451)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Codacy Badge](https://api.codacy.com/project/badge/Grade/a6b8568aab8c4c319a4f58d84cccf7c0)](https://www.codacy.com/manual/jensleitloff/CNN-Sentinel?utm_source=github.com&utm_medium=referral&utm_content=jensleitloff/CNN-Sentinel&utm_campaign=Badge_Grade)

# Dependencies

## seems to work

- tensorflowjs seems to be _old_:
  - this env uses python 3.6 (2016!), and the compatible version of tensorflowjs is 3.18
  - the current tensorflowjs version 4.20 seems to have skipped a lot of tensorflow and python versions

Basically, python 3.6, tf 1.13, keras 2,
followed by docker for conversion:
docker run -it --rm -v "$PWD/convertable:/python" evenchange4/docker-tfjs-converter tensorflowjs_converter --input_format=keras python/input/oldmodel.h5 python/output/

## old attempts

- **training**
  - `conda create -n pycon2 python=3.11 tensorflow=2.15 numpy=1.23 scikit-image gdal tqdm`
  - tensorflow 2.15 (2.16: has no tf.compat.v1.estimator.Exporter: https://stackoverflow.com/questions/78158882/from-tensorflow-compat-v1-import-estimator-as-tf-estimator-importerror-cannot-i )
  - if linux: tensorflow-decision-forests: (google for matching version)
  - numpy 1.23 (1.24: has no np.object: https://stackoverflow.com/questions/75069062/module-numpy-has-no-attribute-object)
  - python 3.11 (3.12 has problems with numpy: https://stackoverflow.com/questions/77364550/attributeerror-module-pkgutil-has-no-attribute-impimporter-did-you-mean)
  - tf_keras? doesn't seem to be required in this setup
  - maybe keras=2.16 (so you can save as .h5 instead of as .keras)
    - but that only saves weights?
  - if you want to try tensorflowjs: version 2.8 scheint mit tensorflow 2.15 kompatibel zu sein; weiß aber nicht, ob damit auch die GPU version funktioniert.
- **conversion**
  - tensorflowjs:
    - probably <= 3.18 (only installable with pip?)
      - not satisfiable with tensorflow 2.15
      - 4.10 will download tensorflow-decision-forests-1.9.0 and tensorflow-2.16.2 and numpy 1.26, destroys previous environment
        - 3.18 also does that, actually!
      - so 4.10 should run in its own environment
        - but requires numpy=1.23
    - `conda create -n tfjsconverter python=3.10 numpy=1.22 h5py=3.11`
    - `pip install tensorflowjs==2.8`
      - wont build h5 wheel
  - better try docker:
    - `mkdir convertable/input  && mkdir convertable/output`
    - `docker run -it --rm  -v "$PWD/convertable:/python"  evenchange4/docker-tfjs-converter  tensorflowjs_converter --input_format=keras python/input/vgg_rgb_transfer_init.01-0.150.keras python/output/`
      - also not good!
  - duplicate environment as described here:https://colab.research.google.com/gist/gaikwadrahul8/8a8883b6e5cc054f2ff0692a13a99505/-8106.ipynb
    - python 3.10
    - tensorflowjs 4.15.0
    - tensorflow 2.15.0
    - tensorflow_decision_forests 1.8.1
    - packaging 23.2
    - numpy 1.23.5
    - h5py 3.9.0
    - keras 2.15.0
    - pandas 1.5.3
    - wheel 0.42.0
    - jax 0.4.21
    - jaxlib 0.4.21
    - `conda create -n tfjsconverter6 python=3.10 numpy=1.22 packaging=23.2 h5py=3.9 wheel=0.42`
    - `pip install --upgrade --upgrade-strategy only-if-needed tensorflowjs==4.15.0`
    - manually remove np.bool and np.object
    - `pip install --upgrade --upgrade-strategy only-if-needed  tensorflow==2.15.0 tensorflow_decision_forests==1.8.1 packaging==23.2 numpy==1.23.5 h5py==3.9.0 keras==2.15.0 pandas==1.5.3 wheel==0.42.0 jax==0.4.21 jaxlib==0.4.21`
    - `tensorflowjs_converter --input_format=keras ./convertable/input/vgg_rgb_transfer_init.01-0.150.keras ./convertable/output/`
  - tried installing with pyenv according to https://github.com/tensorflow/tfjs/tree/master/tfjs-converter, failed

# Analyzing Sentinel-2 satellite data in Python with TensorFlow.Keras

Overview about state-of-the-art land-use classification from satellite data
with CNNs based on an open dataset

## Outline

- [Dependencies](#dependencies)
  - [seems to work](#seems-to-work)
  - [old attempts](#old-attempts)
- [Analyzing Sentinel-2 satellite data in Python with TensorFlow.Keras](#analyzing-sentinel-2-satellite-data-in-python-with-tensorflowkeras)
  - [Outline](#outline)
  - [Scripts you will find here](#scripts-you-will-find-here)
  - [Requirements (what we used)](#requirements-what-we-used)
  - [Frequently asked questions (FAQs)](#frequently-asked-questions-faqs)
  - [Setup environment](#setup-environment)
  - [Our talks about this topic](#our-talks-about-this-topic)
    - [Podcast episode @ TechTiefen](#podcast-episode--techtiefen)
    - [M3 Minds mastering machines 2019 @ Mannheim](#m3-minds-mastering-machines-2019-mannheim)
    - [PyCon.DE 2018 @ Karlsruhe](#pyconde-2018-karlsruhe)
  - [Resources](#resources)
  - [How to get Sentinel-2 data](#how-to-get-sentinel-2-data)
  - [Citation](#citation)

## Scripts you will find here

- `01_split_data_to_train_and_validation.py`: split complete dataset into train
  and validation
- `02_train_rgb_finetuning.py`: train VGG16 or DenseNet201 using RGB data with
  pre-trained weights on ImageNet
- `03_train_rgb_from_scratch.py`: train VGG16 or DenseNet201 from scratch using
  RGB data
- `04_train_ms_finetuning.py`: train VGG16 or DenseNet201 using multispectral
  data with pre-trained weights on ImageNet
- `04_train_ms_finetuning_alternative.py`: an alternative way to train VGG16 or
  DenseNet201 using multispectral data with pre-trained weights on ImageNet
- `05_train_ms_from_scratch.py`: train VGG16 or DenseNet201 from scratch using
  multispectral data
- `06_classify_image.py`: a simple implementation to classify images with
  trained models
- `image_functions.py`: functions for image normalization and a simple
  generator for training data augmentation
- `statistics.py`: a simple implementation to calculate normalization
  parameters (i.e. mean and std of training data)

Additionally you will find the following notebooks:

- `Image_functions.ipynb`: notebook of `image_functions.py`
- `Train_from_Scratch.ipynb`: notebook of `05_train_ms_from_scratch.py`
- `Transfer_learning.ipynb`: notebook of `02_train_rgb_finetuning.py`

## Requirements (what we used)

We have defined the requirements in [requirements.txt](requirements.txt).
We used:

- python 3.6.x
- tensorflow 2.2
- scikit-image (0.14.1)
- gdal (2.2.4) for `06_classify_image.py`

## Frequently asked questions (FAQs)

- **How can I interpret the classification results?** - Please have a look at our answers
  [#3](https://github.com/jensleitloff/CNN-Sentinel/issues/3),
  [#4](https://github.com/jensleitloff/CNN-Sentinel/issues/4), and
  [#6](https://github.com/jensleitloff/CNN-Sentinel/issues/6).
- **Is there a paper I can cite for this repository?** - Please have a look at [Citation](#citation)

## Setup environment

Append conda-forge to your Anaconda channels:

```bash
conda config --append channels conda-forge
```

Create new environment:

```bash
conda create -n pycon scikit-image gdal tqdm
conda activate pycon
pip install tensorflow-gpu
pip install keras
```

(or use tensorflow version of keras, i.e. `from tensorflow import keras`)

See also:

- [Keras](https://keras.io/)

## Our talks about this topic

### Podcast episode @ TechTiefen

- **Title:** "Fernerkundung mit multispektralen Satellitenbildern"
- **Episode:** [Episode 18](https://techtiefen.de/18-fernerkundung-mit-multispektralen-satellitenbildern/)
- **Podcast:** [TechTiefen](https://techtiefen.de) by Nico Kreiling
- **Language:** German (Deutsch)
- **Date:** July 2019

<details><summary>Abstract</summary>
 Jens Leitloff und Felix Riese berichten in Folge 18 von ihrer Forschung am “Institut für Photogrammetrie und Fernerkundung” des Karlsruher Instituts für Technologie. Mit der Bestrebung Nachhaltigkeit zu stärken erforschen die beiden etwa Verfahren, um Wasserqualität anhand von Satellitenaufnahmen zu bewerten oder die Nutzung landwirtschaftlicher Flächen zu kartografieren. Hierfür kommen unterschiedlichste Verfahren zum Einsatz wie Radaraufnahmen oder multispektrale Bilderdaten, die mehr als die drei von Menschen wahrnehmbaren Farbkanäle erfassen. Außerdem geht es um Drohnen, Satelliten und zahlreiche ML-Verfahren wie Transfer- und Aktive Learning. Persönliche Erfahrungen von Jens und Felix im Umgang mit unterschiedlichen Datenmengen runden eine thematisch Breite und anschauliche Folge ab.
</details>

### M3 Minds mastering machines 2019 @ Mannheim

- **Title:** "Satellite Computer Vision mit Keras und Tensorflow - Best practices und beispiele aus der Forschung"
- **Slides:** [Slides](slides/M3-2019_RieseLeitloff_SatelliteCV.pdf)
- **Language:** German (Deutsch)
- **Date:** 15 - 16 May 2019
- **DOI:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4056744.svg)](https://doi.org/10.5281/zenodo.4056744)
- **URL:** [m3-konferenz.de](https://m3-konferenz.de/2019/)

<details><summary>Abstract</summary>
> Im Forschungsfeld des Maschinellen Lernens werden zunehmend leicht zugängliche Framework wie Keras, Tensorflow oder Pytorch verwendet. Hierdurch ist ein Austausch und die Wiederverwendung bestehender (trainierter) neuronaler Netze möglich.
>
> Wir am Institut für Photogrammetrie und Fernerkundung (IPF) des Karlsruher Institut für Technologie (KIT) beschäftigen uns unter anderem mit der Analyse von optischen Satellitendaten. Satellitenprogramme wie Sentinel-2 von Copernicus liefern wöchentliche, weltweite und dabei frei zugängliche multispektrale Bilder, die eine Vielzahl neuartiger Anwendungen ermöglichen. Wir nehmen das zum Anlass, eine interaktive Einführung in die Auswertung dieser Satellitendaten mit Learnings aus unserer täglichen Forschung zu geben. Wir sprechen unter anderem über die folgenden Themen:
>
> * Einfacher Umgang mit georeferenzierten Bilddaten
> * Einführung in Learning-From-Scratch und Transfer Learning mit Keras
> * Anpassung von fertigen Netzen an neue Eingangsdaten (RGB → multispektral)
> * Anschauliche Interpretation von Klassifikationsergebnissen
> * Best Practices aus unserer Forschung, die die Arbeit mit Neuronalen Netzen wesentlich vereinfachen und beschleunigen
> * Code und Daten für die ersten Schritte mit CNNs mit Keras in Python, welche in einem GitHub Repository zur Verfügung gestellt werden
</details>

### PyCon.DE 2018 @ Karlsruhe

- **Title:** "Satellite data is for everyone: insights into modern remote sensing research with open data and Python"
- **Slides:** [Slides](slides/PyCon2018_LeitloffRiese_SatelliteData.pdf)
- **Video:** [youtube.com/watch?v=tKRoMcBeWjQ](https://www.youtube.com/watch?v=tKRoMcBeWjQ)
- **Language:** English
- **Date:** 24 - 28 October 2018
- **DOI:** [![DOI](https://zenodo.org/badge/DOI/10.5281/zenodo.4056516.svg)](https://doi.org/10.5281/zenodo.4056516)
- **URL:** [de.pycon.org](https://de.pycon.org)

<details><summary>Abstract</summary>
> The largest earth observation programme Copernicus (http://copernicus.eu) makes it possible to perform terrestrial observations providing data for all kinds of purposes. One important objective is to monitor the land-use and land-cover changes with the Sentinel-2 satellite mission. These satellites measure the sun reflectance on the earth surface with multispectral cameras (13 channels between 440 nm to 2190 nm). Machine learning techniques like convolutional neural networks (CNN) are able to learn the link between the satellite image (spectrum) and the ground truth (land use class). In this talk, we give an overview about the state-of-the-art land-use classification with CNNs based on an open dataset.
>
> We use different out-of-box CNNs for the Keras deep learning library (https://keras.io/). All networks are either included in Keras itself or are available from Github repositories. We show the process of transfer learning for the RGB datasets. Furthermore, the minimal changes required to apply commonly used CNNs to multispectral data are demonstrated. Thus, the interested audience will be able to perform their own classification of remote sensing data within a very short time. Results of different network structures are visually compared. Especially the differences of transfer learning and learning from scratch are demonstrated. This also includes the amount of necessary training epochs, progress of training and validation error and visual comparison of the results of the trained networks. Finally, we give a quick overview about the current research topics including recurrent neural networks for spatio-temporal land-use classification and further applications of multi- and hyperspectral data, e.g. for the estimation of water parameters and soil characteristics.
</details>

## Resources

**This talk:**

- EuroSAT Data (Sentinel-2, [Link](http://madm.dfki.de/downloads))

**Platforms for datasets:**

- HyperLabelMe: a Web Platform for Benchmarking Remote Sensing Image Classifiers ([Link](http://hyperlabelme.uv.es/))
- GRSS Data and Algorithm Standard Evaluation (DASE) website ([Link](http://dase.ticinumaerospace.com/))

**Datasets:**

- ISPRS 2D labeling challenge ([Link](http://www2.isprs.org/commissions/comm3/wg4/semantic-labeling.html))
- UC Merced Land Use Dataset ([Link](http://weegee.vision.ucmerced.edu/datasets/landuse.html))
- AID: A Benchmark Dataset for Performance Evaluation of Aerial Scene Classification ([Link](https://captain-whu.github.io/AID/))
- NWPU-RESISC45 (RGB, [Link](http://www.escience.cn/people/JunweiHan/NWPU-RESISC45.html))
- Zurich Summer Dataset (RGB, [Link](https://sites.google.com/site/michelevolpiresearch/data/zurich-dataset))
- **Note**: Many German state authorities offer free geodata (high resolution images, land use/cover vector data, ...) over their geoportals. You can find an overview of all geoportals here ([geoportals](https://www.geoportal.nrw/geoportale_bundeslaender_nachbarstaaten))

**Image Segmentation Resources:**

- More than 100 combinations for image segmentation routines with Keras and pretrained weights for endcoding phase ([Segmentation Models](https://github.com/qubvel/segmentation_models))
- Another source for image segmentation with Keras including pretrained weights ([Keras-FCN](https://github.com/aurora95/Keras-FCN))
- Great link collection of image segmantation networks and datasets ([Link](https://github.com/mrgloom/awesome-semantic-segmentation))
- Free land use vector data of NRW ([BasisDLM](https://www.bezreg-koeln.nrw.de/brk_internet/geobasis/landschaftsmodelle/basis_dlm/index.html) or [openNRW](https://open.nrw/en/node/154))

**Other:**

- DeepHyperX - Deep learning for Hyperspectral imagery: [gitlab.inria.fr/naudeber/DeepHyperX/](https://gitlab.inria.fr/naudeber/DeepHyperX/)

## How to get Sentinel-2 data

1. Register at Copernicus [Open Access Hub](https://scihub.copernicus.eu/dhus/#/home) or [EarthExplorer](https://earthexplorer.usgs.gov/)
2. Find your region
3. Choose tile(s) (→ area) and date
   - Less tiles makes things easier
   - Less clouds in the image are better
   - Consider multiple dates for classes like “annual crop”
4. Download L1C data
5. Decide of you want to apply L2A atmospheric corrections
   - Your CNN might be able to do this by itself
   - If you want to correct, use [Sen2Cor](http://step.esa.int/main/third-party-plugins-2/sen2cor/)
6. Have fun with the data

## Citation

Jens Leitloff and Felix M. Riese, "Examples for CNN training and classification on Sentinel-2 data", Zenodo, [10.5281/zenodo.3268451](http://doi.org/10.5281/zenodo.3268451), 2018.

```tex
@misc{leitloff2018examples,
    author = {Leitloff, Jens and Riese, Felix~M.},
    title = {{Examples for CNN training and classification on Sentinel-2 data}},
    year = {2018},
    DOI = {10.5281/zenodo.3268451},
    publisher = {Zenodo},
    howpublished = {\href{http://doi.org/10.5281/zenodo.3268451}{http://doi.org/10.5281/zenodo.3268451}}
}
```
