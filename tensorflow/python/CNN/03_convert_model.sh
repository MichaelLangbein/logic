#! /bin/bash
docker run -it --rm  -v "$PWD/models:/python"  evenchange4/docker-tfjs-converter  tensorflowjs_converter --input_format=keras python/input/convertme.h5 python/output/