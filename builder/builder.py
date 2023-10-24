# Copyright (c) Microsoft Corporation.
# SPDX-License-Identifier: Apache-2.0

# DeepSpeed Team

import os
import subprocess
from setuptools import Extension
from setuptools.command.build_ext import build_ext
from packaging import version as pkg_version


def installed_cuda_version():
    cuda_home = os.environ.get("CUDA_HOME", None)
    if cuda_home is None:
        import torch.utils.cpp_extension
        cuda_home = torch.utils.cpp_extension.CUDA_HOME
    assert cuda_home is not None, "CUDA_HOME does not exist, unable to compile CUDA op(s)"
    output = subprocess.check_output([cuda_home + "/bin/nvcc", "-V"],
                                     universal_newlines=True)
    output_split = output.split()
    release_idx = output_split.index("release")
    release = output_split[release_idx + 1].replace(',', '')
    return pkg_version.parse(release)


def validate_arch_list(cuda_arch_list: str):
    cuda_version = installed_cuda_version()
    cuda_arch_list = cuda_arch_list.split(';')
    for arch in cuda_arch_list:
        if arch == 'native':
            continue
        try:
            arch = int(arch)
        except ValueError:
            raise ValueError(
                f"Invalid CUDA_ARCH_LIST: {cuda_arch_list}. "
                "CUDA_ARCH_LIST must be a list of integers or 'native'.")

        # [error] if cuda < 11.8 and arch is >= 89
        if cuda_version < pkg_version.parse('11.8'):
            assert arch < 89, f"Compute capability of {arch} is not supported for CUDA {cuda_version}"

        # [error] if cuda == 11.8 and arch > 90
        if cuda_version == pkg_version.parse('11.8'):
            assert arch <= 90, f"Compute capability of {arch} is not supported for CUDA {cuda_version}"

        # [error] min arch is 80
        assert arch >= 80, f"Compute capability less than 80 is not supported for DeepSpeed kernels"


class CMakeExtension(Extension):
    def __init__(self, name, sources=[]):
        super().__init__(name, sources)


class CMakeBuild(build_ext):
    def run(self):
        for ext in self.extensions:
            self.build_extension(ext)

    def build_extension(self, ext):
        # Build in kernel unique sub-directory inside temp build directory
        abs_build_temp = os.path.abspath(self.build_temp)
        abs_build_temp = os.path.join(abs_build_temp, ext.name)

        # Pass through CUDA_ARCH_LIST if defined, otherwise fall back to native
        cuda_arch_list = os.environ.get('CUDA_ARCH_LIST', 'native')
        validate_arch_list(cuda_arch_list)

        # Destination path for final binaries
        abs_build_lib = os.path.join(os.path.abspath(self.build_lib),
                                     "dskernels")

        subprocess.check_call(['cmake', '-B', abs_build_temp, 
                               f'-DLIB_OUTPUT_DIR={abs_build_lib}',
                               f'-DCUDA_ARCH_LIST={cuda_arch_list}'],
                               cwd=ext.source)
        subprocess.check_call(['make', '-j'], cwd=abs_build_temp)
