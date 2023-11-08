set -ex

rm -rf dist

#export DS_KERNELS_MAKE_JOBS=10

ts=$(date +%s)
DS_KERNELS_BUILD_STRING=".dev${ts}" CUDA_ARCH_LIST="80;86" python setup.py bdist_wheel

# rename whl to ensure portability
fname=$(ls dist)
nname=$(echo $fname | sed 's/cp[0-9]\+-cp[0-9]\+/py3-none/' | sed 's/linux/manylinux1/')
mv "dist/$fname" "dist/$nname"

twine upload dist/*.whl
