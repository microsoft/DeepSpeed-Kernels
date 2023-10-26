[![License Apache 2.0](https://badgen.net/badge/license/apache2.0/blue)](https://github.com/Microsoft/DeepSpeed/blob/master/LICENSE)
[![PyPI version](https://badge.fury.io/py/deepspeed-kernels.svg)](https://pypi.org/project/deepspeed-kernels/)

# DeepSpeed Kernels

DeepSpeed-Kernels is a backend library that is used to power [DeepSpeed-Inference](https://github.com/microsoft/deepspeed) and [DeepSpeed-MII](https://github.com/microsoft/deepspeed-mii) to achieve accelerated text-generation inference. This library is not intended to be an independent user package, but is open-source to benefit the community and show how DeepSpeed is accelerating text-generation.

# Installation

## PyPI

If your environment supports it you can quickly install DeepSpeed-Kernels from [PyPI](https://pypi.org/project/deepspeed-kernels/) (see below). We've tested the portability of the PyPI release on A100, A6000, and H100.

The release on PyPI should work with the following assumptions about your environment:
* NVIDIA GPU(s) with compute capability of: 8.0, 8.6, 8.9, 9.0
* CUDA 11.6+
* Ubuntu 20+

```bash
pip install deepspeed-kernels
```

## Source
If the PyPI release does not work for you we recommend installing from source which can take several minutes:
```bash
pip install -v .
```

## Advanced

You can create a pre-compiled portable wheel that supports different CUDA architectures via the `CUDA_ARCH_LIST` environment variable. By default the kernels will be compiled using the `native` compute capability. If you want to compile for more than one you can set the `CUDA_ARCH_LIST` environment variable. We currently only support Ampere and above architectures (i.e., 8.0+). See example below to build for GPUs like A100 and A6000:
```bash
CUDA_ARCH_LIST="80;86;89;90" python setup.py bdist_wheel
```
