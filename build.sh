set -ex

# ensure all submodules are present before build
git submodule update --init --recursive

python setup.py bdist_wheel
