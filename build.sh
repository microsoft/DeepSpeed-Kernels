set -ex

# set CUDA_ARCH_LIST if desired, otherwise falls back to native
CUDA_ARCH_LIST="80;86" python setup.py bdist_wheel
