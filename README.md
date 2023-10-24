[![License Apache 2.0](https://badgen.net/badge/license/apache2.0/blue)](https://github.com/Microsoft/DeepSpeed/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/deepspeed-kernels.svg)](https://pypi.org/project/deepspeed-kernels/)

# DeepSpeed Kernels

TODO: add short description of what this repo is for

# Installation

## Installation from PyPI

If your environment supports it you can quickly install DeepSpeed-Kernels from [PyPI](https://pypi.org/project/deepspeed-kernels/) (see below). 

The release on PyPI should work with the following assumptions about your environment:
* NVIDIA GPU(s) with compute capability of: 8.0, 8.6
* CUDA 11.7+
* Ubuntu 20+

```bash
pip install deepspeed-kernels
```

## Installation from source
If the PyPI release does not work for you we recommend installing from source which can take several minutes:
```bash
pip install -v .
```

## Advanced Installation

You can create a pre-compiled portable wheel that supports different CUDA architectures via the `CUDA_ARCH_LIST` environment variable. By default the kernels will be compiled using the `native` compute capability. If you want to compile for more than one you can set the `CUDA_ARCH_LIST` environment variable. We currently only support Ampere and above architectures (i.e., 8.0+). See example below to build for GPUs like A100 and A6000:
```bash
CUDA_ARCH_LIST="80;86" python setup.py bdist_wheel
```
