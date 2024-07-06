#! /bin/bash
# remarkably, this works with *.h5 models from both tensorflow 1.x and 2.x
# even though tensorflowjs here is pretty old (version 3.18, using python 3.6 and tensorflow 1.x)
#
# PS: a new version of tensorflowjs (4.20) is available on pip, but throws that weird error:
# AttributeError: module 'tensorflow.compat.v1' has no attribute 'estimator'

docker run -it --rm  -v "$PWD/models:/python"  evenchange4/docker-tfjs-converter  tensorflowjs_converter --input_format=keras python/input/convertme.h5 python/output/