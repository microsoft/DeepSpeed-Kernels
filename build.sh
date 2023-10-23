set -ex

# ensure all submodules are present before build
git submodule update --init --recursive

# set CUDA_ARCH_LIST if desired, otherwise falls back to native
CUDA_ARCH_LIST="86" python setup.py bdist_wheel
