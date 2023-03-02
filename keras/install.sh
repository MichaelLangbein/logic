#! /bin/bash
set -x           # for debugging only: print out current line before executing it
set -o errexit   # abort on nonzero exitstatus
set -o nounset   # abort on unbound variable
set -o pipefail  # don't hide errors within pipes


# based on https://www.tensorflow.org/install/pip

conda create --name tf python=3.9
conda deactivate
conda activate tf
conda install -y -c conda-forge cudatoolkit=11.2.2 cudatoolkit-dev cudnn=8.1.0 

export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
echo 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh

pip install --upgrade pip
pip install tensorflow==2.11.*


# Install NVCC
#conda install -y -c nvidia cuda-nvcc=11.3.58
# Configure the XLA cuda directory
mkdir -p $CONDA_PREFIX/etc/conda/activate.d
printf 'export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$CONDA_PREFIX/lib/\nexport XLA_FLAGS=--xla_gpu_cuda_data_dir=$CONDA_PREFIX/lib/\n' > $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
source $CONDA_PREFIX/etc/conda/activate.d/env_vars.sh
# Copy libdevice file to the required path
mkdir -p $CONDA_PREFIX/lib/nvvm/libdevice
cp $CONDA_PREFIX/lib/libdevice.10.bc $CONDA_PREFIX/lib/nvvm/libdevice/


# verify gpu setup 
python3 -c "import tensorflow as tf; print(tf.config.list_physical_devices('GPU'))"


conda install -y ipykernel matplotlib
