# Installation

Basic installation, this should finish within 2-5 minutes:
```bash
pip install -v .
```

Create a python whl:
```bash
python setup.py bdist_wheel
```

By default the kernels will be compiled using the `native` compute capability. If you want to compile for more than one you can set the `CUDA_ARCH_LIST` environment variable. See example below:
```bash
CUDA_ARCH_LIST="80;86" python setup.py bdist_wheel
```
